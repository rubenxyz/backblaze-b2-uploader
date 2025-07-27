#!/usr/bin/env python3
"""
Backblaze B2 Image Uploader

A Python script that uploads images from a local input directory to a Backblaze B2 bucket,
providing comprehensive logging and link generation. Uses 1Password CLI for secure authentication.
"""

import argparse
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List

from loguru import logger

from b2_auth import B2Auth, B2AuthError, authenticate_b2
from config import Config
from utils import (
    create_timestamped_output_dir,
    generate_failure_report,
    generate_json_log,
    generate_link_file,
    run_b2_command
)


def setup_logging(verbose: bool = False):
    """Configure logging for the application."""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    log_level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )


def sync_operation(verbose: bool = False, dry_run: bool = False) -> int:
    """Execute sync operation to mirror input directory to B2 bucket."""
    start_time = time.time()
    
    try:
        logger.info("Starting B2 sync operation")
        
        # Validate environment
        if not Config.validate_environment():
            logger.error("Environment validation failed")
            return 1
        
        # Authenticate with B2
        auth = authenticate_b2()
        bucket_name = auth.get_bucket_name()
        
        # Create output directory
        output_dir = create_timestamped_output_dir()
        
        # Prepare sync command
        input_path = Config.get_input_path()
        sync_command = [
            Config.B2_CLI, "sync",
            str(input_path),
            f"b2://{bucket_name}/"
        ]
        
        if dry_run:
            sync_command.append("--dry-run")
            logger.info("DRY RUN MODE - No actual changes will be made")
        
        logger.info(f"Executing sync command: {' '.join(sync_command)}")
        
        # Execute sync
        return_code, stdout, stderr = run_b2_command(sync_command)
        
        execution_time = time.time() - start_time
        
        if return_code != 0:
            logger.error(f"B2 sync failed with return code {return_code}")
            logger.error(f"Error output: {stderr}")
            
            # Generate error report
            errors = [{
                'file': 'sync_operation',
                'error_type': 'B2SyncFailure',
                'error_message': stderr,
                'timestamp': datetime.now().isoformat()
            }]
            
            generate_failure_report(output_dir, errors, "sync")
            return return_code
        
        # Parse sync output
        from utils import parse_b2_sync_output
        files_processed = parse_b2_sync_output(stdout)
        
        # Generate output files
        generate_json_log(
            output_dir=output_dir,
            operation="sync",
            files_processed=files_processed,
            errors=[],
            execution_time=execution_time,
            bucket_name=bucket_name
        )
        
        generate_link_file(output_dir, files_processed, bucket_name)
        
        # Log summary
        logger.info(f"Sync completed successfully in {execution_time:.2f} seconds")
        logger.info(f"Files processed: {len(files_processed)}")
        logger.info(f"Output directory: {output_dir}")
        
        return 0
        
    except B2AuthError as e:
        logger.error(f"Authentication error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during sync: {e}")
        return 1


def clean_operation(force: bool = False, dry_run: bool = False) -> int:
    """Execute clean operation to remove all files from B2 bucket."""
    start_time = time.time()
    
    try:
        logger.info("Starting B2 clean operation")
        
        # Validate environment
        if not Config.validate_environment():
            logger.error("Environment validation failed")
            return 1
        
        # Authenticate with B2
        auth = authenticate_b2()
        bucket_name = auth.get_bucket_name()
        
        # Create output directory
        output_dir = create_timestamped_output_dir()
        
        # Check if bucket exists and is accessible
        bucket_check_command = [Config.B2_CLI, "ls", f"b2://{bucket_name}"]
        return_code, stdout, stderr = run_b2_command(bucket_check_command)
        
        if return_code != 0:
            logger.error(f"Failed to access bucket '{bucket_name}'")
            logger.error(f"Error: {stderr}")
            return return_code
        
        # List current files for confirmation
        list_command = [Config.B2_CLI, "ls", "--long", f"b2://{bucket_name}"]
        return_code, stdout, stderr = run_b2_command(list_command)
        
        if return_code != 0:
            logger.error("Failed to list bucket contents")
            logger.error(f"Error: {stderr}")
            return return_code
        
        # Count files
        file_count = len([line for line in stdout.split('\n') if line.strip() and not line.startswith('--')])
        
        if not force and not dry_run:
            print(f"\nWARNING: This will permanently delete {file_count} files from bucket '{bucket_name}'")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                logger.info("Clean operation cancelled by user")
                return 0
        
        if dry_run:
            logger.info(f"DRY RUN: Would delete {file_count} files from bucket '{bucket_name}'")
            return 0
        
        # Execute clean command
        clean_command = [
            Config.B2_CLI, "rm",
            "--versions",
            "--recursive",
            f"b2://{bucket_name}"
        ]
        
        logger.info(f"Executing clean command: {' '.join(clean_command)}")
        
        return_code, stdout, stderr = run_b2_command(clean_command)
        
        execution_time = time.time() - start_time
        
        if return_code != 0:
            logger.error(f"B2 clean failed with return code {return_code}")
            logger.error(f"Error output: {stderr}")
            return return_code
        
        # Clean up any unfinished large files
        cancel_command = [Config.B2_CLI, "cancel-all-unfinished-large-files", bucket_name]
        cancel_return_code, cancel_stdout, cancel_stderr = run_b2_command(cancel_command)
        
        if cancel_return_code == 0:
            logger.info("Cleaned up unfinished large files")
        
        # Generate log
        files_processed = [{
            'local_path': '',
            'b2_key': f'bucket://{bucket_name}',
            'action': 'delete_all',
            'status': 'success',
            'file_count': file_count
        }]
        
        generate_json_log(
            output_dir=output_dir,
            operation="clean",
            files_processed=files_processed,
            errors=[],
            execution_time=execution_time,
            bucket_name=bucket_name,
            files_deleted=file_count
        )
        
        logger.info(f"Clean completed successfully in {execution_time:.2f} seconds")
        logger.info(f"Files deleted: {file_count}")
        logger.info(f"Output directory: {output_dir}")
        
        return 0
        
    except B2AuthError as e:
        logger.error(f"Authentication error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during clean: {e}")
        return 1


def main():
    """Main entry point for the B2 uploader application."""
    parser = argparse.ArgumentParser(
        description="Backblaze B2 Image Uploader - Sync images to B2 bucket with 1Password authentication",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python b2_uploader.py                    # Sync files to B2 bucket
  python b2_uploader.py sync              # Explicit sync operation
  python b2_uploader.py sync --dry-run    # Preview sync without making changes
  python b2_uploader.py clean             # Remove all files from bucket (with confirmation)
  python b2_uploader.py clean --force     # Remove all files without confirmation
  python b2_uploader.py clean --dry-run   # Preview clean without making changes
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Sync command
    sync_parser = subparsers.add_parser(
        'sync',
        help='Synchronize files from input directory to B2 bucket'
    )
    sync_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without making them'
    )
    sync_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    # Clean command
    clean_parser = subparsers.add_parser(
        'clean',
        help='Remove all files from B2 bucket'
    )
    clean_parser.add_argument(
        '--force',
        action='store_true',
        help='Skip confirmation prompt'
    )
    clean_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview what would be deleted without making changes'
    )
    clean_parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    verbose = getattr(args, 'verbose', False)
    setup_logging(verbose)
    
    # Default to sync if no command specified
    if not args.command:
        args.command = 'sync'
        args.dry_run = False
        args.verbose = verbose
    
    try:
        if args.command == 'sync':
            return sync_operation(verbose=args.verbose, dry_run=args.dry_run)
        elif args.command == 'clean':
            return clean_operation(force=args.force, dry_run=args.dry_run)
        else:
            parser.print_help()
            return 1
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 