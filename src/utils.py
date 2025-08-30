"""Utility functions for B2 sync operations."""

import json
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger

from .config import Config


def create_timestamped_output_dir(base_dir: Path) -> Path:
    """Create a timestamped output directory for this run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = base_dir / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created output directory: {output_dir}")
    return output_dir


def parse_b2_sync_output(output: str) -> List[Dict[str, str]]:
    """Parse B2 sync command output to extract file information."""
    files = []
    lines = output.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Parse different types of sync output lines
        # Example: "upload: USER-FILES/04.INPUT/test.jpg -> b2://fal-bucket/test.jpg"
        upload_match = re.match(r'upload:\s+(.+?)\s+->\s+b2://[^/]+/(.+)', line)
        if upload_match:
            local_path = upload_match.group(1)
            b2_key = upload_match.group(2)
            files.append({
                'local_path': local_path,
                'b2_key': b2_key,
                'action': 'upload',
                'status': 'success',
                'sync_time': datetime.now().isoformat()
            })
            continue
        
        # Example: "update: USER-FILES/04.INPUT/test.jpg -> b2://fal-bucket/test.jpg"
        update_match = re.match(r'update:\s+(.+?)\s+->\s+b2://[^/]+/(.+)', line)
        if update_match:
            local_path = update_match.group(1)
            b2_key = update_match.group(2)
            files.append({
                'local_path': local_path,
                'b2_key': b2_key,
                'action': 'update',
                'status': 'success',
                'sync_time': datetime.now().isoformat()
            })
            continue
        
        # Example: "delete: b2://fal-bucket/old_file.jpg"
        delete_match = re.match(r'delete:\s+b2://[^/]+/(.+)', line)
        if delete_match:
            b2_key = delete_match.group(1)
            files.append({
                'local_path': '',
                'b2_key': b2_key,
                'action': 'delete',
                'status': 'success',
                'sync_time': datetime.now().isoformat()
            })
            continue
        
        # Example: "skip: USER-FILES/04.INPUT/test.jpg -> b2://fal-bucket/test.jpg (already exists)"
        skip_match = re.match(r'skip:\s+(.+?)\s+->\s+b2://[^/]+/(.+)', line)
        if skip_match:
            local_path = skip_match.group(1)
            b2_key = skip_match.group(2)
            files.append({
                'local_path': local_path,
                'b2_key': b2_key,
                'action': 'skip',
                'status': 'success',
                'sync_time': datetime.now().isoformat()
            })
            continue
    
    return files


def get_actual_download_urls(bucket_name: str) -> List[str]:
    """Get actual download URLs from B2 for all files in the bucket."""
    urls = []
    try:
        # Get list of files in bucket
        list_command = [Config.B2_CLI, "ls", f"b2://{bucket_name}"]
        return_code, stdout, stderr = run_b2_command(list_command)
        
        if return_code != 0:
            logger.error(f"Failed to list bucket contents: {stderr}")
            return urls
        
        # For each file, construct the download URL
        # The URL format is: https://{endpoint}.backblazeb2.com/file/{bucket_name}/{filename}
        # We need to determine the correct endpoint (f001, f003, etc.)
        
        # Try to get the endpoint from account info
        account_command = [Config.B2_CLI, "account", "get"]
        account_return_code, account_stdout, account_stderr = run_b2_command(account_command)
        
        endpoint = "f003"  # Default fallback
        if account_return_code == 0:
            try:
                account_data = json.loads(account_stdout)
                download_url = account_data.get('downloadUrl', '')
                # Extract endpoint from URL: https://f003.backblazeb2.com
                import re
                endpoint_match = re.search(r'https://([^.]+)\.backblazeb2\.com', download_url)
                if endpoint_match:
                    endpoint = endpoint_match.group(1)
            except json.JSONDecodeError:
                pass
        
        # Now construct URLs for all files using the correct endpoint
        for line in stdout.strip().split('\n'):
            if line.strip():
                filename = line.strip()
                download_url = f"https://{endpoint}.backblazeb2.com/file/{bucket_name}/{filename}"
                urls.append(download_url)
                    
    except Exception as e:
        logger.error(f"Error getting download URLs: {e}")
    
    return urls


def generate_link_files(output_dir: Path, files_processed: List[Dict[str, str]], bucket_name: str) -> Path:
    """Generate individual link files for each uploaded file with B2 friendly URLs."""
    # Get actual download URLs from B2
    urls = get_actual_download_urls(bucket_name)
    
    files_created = 0
    
    if urls:
        # Create individual text files for each URL
        for url in urls:
            # Extract filename from URL
            filename_match = re.search(r'/([^/]+)$', url)
            if filename_match:
                original_filename = filename_match.group(1)
                # Remove extension and add .txt
                base_name = Path(original_filename).stem
                link_filename = f"{base_name}.txt"
                link_file_path = output_dir / link_filename
                
                # Write the friendly URL to the individual file
                with open(link_file_path, 'w') as f:
                    f.write(url)
                
                files_created += 1
                logger.debug(f"Created link file: {link_file_path}")
    else:
        logger.warning("No URLs found, using fallback method")
        # Fallback to files_processed if available
        for file_info in files_processed:
            b2_key = file_info.get('b2_key', '')
            if b2_key and file_info.get('action') in ['upload', 'update']:
                # Extract just the filename from the b2_key
                filename = Path(b2_key).name
                base_name = Path(filename).stem
                link_filename = f"{base_name}.txt"
                link_file_path = output_dir / link_filename
                
                # Generate the friendly URL (using f003 as default)
                public_url = f"https://f003.backblazeb2.com/file/{bucket_name}/{b2_key}"
                
                # Write the friendly URL to the individual file
                with open(link_file_path, 'w') as f:
                    f.write(public_url)
                
                files_created += 1
                logger.debug(f"Created link file: {link_file_path}")
    
    logger.info(f"Generated {files_created} individual link files in: {output_dir}")
    return output_dir


def generate_json_log(
    output_dir: Path,
    operation: str,
    files_processed: List[Dict[str, str]],
    errors: List[Dict[str, str]],
    execution_time: float,
    **kwargs
) -> Path:
    """Generate comprehensive JSON log file."""
    timestamp = datetime.now().isoformat()
    
    # Calculate statistics
    stats = {
        "files_uploaded": len([f for f in files_processed if f.get('action') == 'upload']),
        "files_updated": len([f for f in files_processed if f.get('action') == 'update']),
        "files_deleted": len([f for f in files_processed if f.get('action') == 'delete']),
        "files_skipped": len([f for f in files_processed if f.get('action') == 'skip']),
        "files_failed": len([f for f in files_processed if f.get('status') == 'failed']),
    }
    
    # Add file size information for uploaded/updated files
    for file_info in files_processed:
        if file_info.get('action') in ['upload', 'update'] and file_info.get('local_path'):
            local_path = Path(file_info['local_path'])
            if local_path.exists():
                try:
                    file_info['file_size_bytes'] = local_path.stat().st_size
                except Exception:
                    file_info['file_size_bytes'] = 0
    
    log_data = {
        "run_metadata": {
            "timestamp": timestamp,
            "operation": operation,
            "total_files": len(files_processed),
            "execution_time_seconds": execution_time,
            **stats,
            **kwargs
        },
        "files_processed": files_processed,
        "errors": errors
    }
    
    log_file = output_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{operation}_log.json"
    
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
    
    logger.info(f"Generated JSON log: {log_file}")
    return log_file


def generate_failure_report(output_dir: Path, errors: List[Dict[str, str]], operation: str) -> Optional[Path]:
    """Generate human-readable failure report if there are errors."""
    if not errors:
        return None
    
    timestamp = datetime.now()
    failure_file = output_dir / "FAILURE.md"
    
    with open(failure_file, 'w') as f:
        f.write("# Sync Failure Report\n")
        f.write(f"**Date**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Operation**: {operation}\n\n")
        
        f.write("## Summary\n")
        f.write(f"- **Failed Files**: {len(errors)}\n\n")
        
        f.write("## Failed Files\n")
        for error in errors:
            file_path = error.get('file', 'Unknown')
            error_type = error.get('error_type', 'Unknown')
            error_message = error.get('error_message', 'No details available')
            
            f.write(f"### {file_path}\n")
            f.write(f"- **Error**: {error_message}\n")
            f.write(f"- **Type**: {error_type}\n\n")
        
        f.write("## Next Steps\n")
        f.write("1. Fix the identified issues with failed files\n")
        f.write("2. Re-run the sync script to update changes\n")
    
    logger.warning(f"Generated failure report: {failure_file}")
    return failure_file


def run_b2_command(command: List[str], timeout: Optional[int] = None) -> Tuple[int, str, str]:
    """Run a B2 CLI command and return results."""
    if timeout is None:
        timeout = 1800  # Default 30 minutes
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        logger.error(f"B2 command timed out after {timeout} seconds")
        return -1, "", "Command timed out"
    except Exception as e:
        logger.error(f"Failed to run B2 command: {e}")
        return -1, "", str(e)


def validate_file_size(file_path: Path, max_size: int) -> bool:
    """Validate that file size is within limits."""
    try:
        file_size = file_path.stat().st_size
        if file_size > max_size:
            logger.warning(f"File {file_path} exceeds size limit: {file_size} bytes")
            return False
        return True
    except Exception as e:
        logger.warning(f"Could not validate file size for {file_path}: {e}")
        return False


def get_supported_files(input_dir: Path, config: 'Config') -> List[Path]:
    """Get list of supported image files from input directory."""
    supported_files = []
    
    for file_path in input_dir.rglob('*'):
        if file_path.is_file() and config.is_supported_format(file_path):
            if validate_file_size(file_path, config.max_file_size):
                supported_files.append(file_path)
            else:
                logger.warning(f"Skipping {file_path} due to size limit")
    
    return supported_files