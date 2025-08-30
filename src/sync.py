"""Main B2 sync operations."""

import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from loguru import logger

from .auth import B2AuthError, authenticate_b2
from .config import Config
from .utils import (
    create_timestamped_output_dir,
    generate_failure_report,
    generate_json_log,
    generate_link_files,
    parse_b2_sync_output,
    run_b2_command
)


class B2Sync:
    """Handle B2 sync operations."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize with configuration."""
        self.config = config or Config()
        
    def sync_operation(self, dry_run: bool = False) -> int:
        """Execute sync operation to mirror input directory to B2 bucket."""
        start_time = time.time()
        
        try:
            logger.info("Starting B2 sync operation")
            
            # Validate environment
            if not Config.validate_environment():
                logger.error("Environment validation failed")
                return 1
            
            # Authenticate with B2
            auth = authenticate_b2(self.config)
            bucket_name = auth.get_bucket_name()
            
            # Create output directory with timestamp
            output_dir = create_timestamped_output_dir(Config.get_output_path())
            
            # Prepare sync command
            input_path = Config.get_input_path()
            sync_command = [
                Config.B2_CLI, "sync",
                "--replace-newer",  # Allow older local files to replace newer destination files
                "--delete",  # Delete files from destination that are not in source (true mirroring)
            ]
            
            # Add exclusion patterns
            for pattern in self.config.exclude_patterns:
                sync_command.extend(["--exclude-regex", pattern])
            
            sync_command.extend([
                str(input_path),
                f"b2://{bucket_name}/"
            ])
            
            if dry_run:
                sync_command.append("--dry-run")
                logger.info("DRY RUN MODE - No actual changes will be made")
            
            logger.info(f"Executing sync command: {' '.join(sync_command)}")
            
            # Execute sync
            return_code, stdout, stderr = run_b2_command(sync_command, self.config.sync_timeout)
            
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
            
            generate_link_files(output_dir, files_processed, bucket_name)
            
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
    
    def clean_operation(self, force: bool = False, dry_run: bool = False) -> int:
        """Execute clean operation to remove all files from B2 bucket."""
        start_time = time.time()
        
        try:
            logger.info("Starting B2 clean operation")
            
            # Validate environment
            if not Config.validate_environment():
                logger.error("Environment validation failed")
                return 1
            
            # Authenticate with B2
            auth = authenticate_b2(self.config)
            bucket_name = auth.get_bucket_name()
            
            # Create output directory
            output_dir = create_timestamped_output_dir(Config.get_output_path())
            
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