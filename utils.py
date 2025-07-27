import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from loguru import logger

from config import Config


def create_timestamped_output_dir() -> Path:
    """Create a timestamped output directory for this run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Config.get_output_path() / timestamp
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
        # Example: "upload: 01.input/test.jpg -> b2://fal-bucket/test.jpg"
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
        
        # Example: "update: 01.input/test.jpg -> b2://fal-bucket/test.jpg"
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
        
        # Example: "skip: 01.input/test.jpg -> b2://fal-bucket/test.jpg (already exists)"
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
        
        # Example: "error: 01.input/corrupted.jpg -> b2://fal-bucket/corrupted.jpg (file error)"
        error_match = re.match(r'error:\s+(.+?)\s+->\s+b2://[^/]+/(.+)', line)
        if error_match:
            local_path = error_match.group(1)
            b2_key = error_match.group(2)
            files.append({
                'local_path': local_path,
                'b2_key': b2_key,
                'action': 'error',
                'status': 'failed',
                'sync_time': datetime.now().isoformat(),
                'error_message': line
            })
            continue
    
    return files


def extract_urls_from_sync_output(output: str) -> Dict[str, str]:
    """Extract public URLs from B2 sync output."""
    urls = {}
    pattern = re.compile(Config.URL_PATTERN)
    
    for line in output.split('\n'):
        match = pattern.search(line)
        if match:
            # Extract filename from the line and map to URL
            # This is a simplified approach - in practice, you might need more complex parsing
            url = match.group(1)
            # Try to extract filename from the URL or surrounding context
            filename_match = re.search(r'/([^/]+)$', url)
            if filename_match:
                filename = filename_match.group(1)
                urls[filename] = url
    
    return urls


def get_file_info(file_path: Path) -> Dict[str, any]:
    """Get file information for logging."""
    try:
        stat = file_path.stat()
        return {
            'file_size_bytes': stat.st_size,
            'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'is_file': file_path.is_file(),
            'is_dir': file_path.is_dir()
        }
    except Exception as e:
        logger.warning(f"Could not get file info for {file_path}: {e}")
        return {}


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


def generate_link_file(output_dir: Path, files_processed: List[Dict[str, str]], bucket_name: str) -> Path:
    """Generate human-readable link file."""
    timestamp = datetime.now()
    
    link_file = output_dir / f"{timestamp.strftime('%Y%m%d_%H%M%S')}_bucket-links.txt"
    
    with open(link_file, 'w') as f:
        f.write(f"# Backblaze B2 Sync Links - {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# Bucket: {bucket_name}\n")
        f.write(f"# Total Files: {len(files_processed)}\n")
        
        # Count actions
        actions = {}
        for file_info in files_processed:
            action = file_info.get('action', 'unknown')
            actions[action] = actions.get(action, 0) + 1
        
        action_summary = ", ".join([f"{k}={v}" for k, v in actions.items()])
        f.write(f"# Sync Action: {action_summary}\n\n")
        
        # Write file links
        for file_info in files_processed:
            b2_key = file_info.get('b2_key', '')
            if b2_key:
                f.write(f"{b2_key}\n")
                # Generate public URL (this is a simplified version)
                public_url = f"https://f001.backblazeb2.com/file/{bucket_name}/{b2_key}"
                f.write(f"{public_url}\n\n")
    
    logger.info(f"Generated link file: {link_file}")
    return link_file


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


def run_b2_command(command: List[str], timeout: int = None) -> Tuple[int, str, str]:
    """Run a B2 CLI command and return results."""
    if timeout is None:
        timeout = Config.SYNC_TIMEOUT
    
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


def validate_file_size(file_path: Path) -> bool:
    """Validate that file size is within B2 limits."""
    try:
        file_size = file_path.stat().st_size
        if file_size > Config.MAX_FILE_SIZE:
            logger.warning(f"File {file_path} exceeds 5GB limit: {file_size} bytes")
            return False
        return True
    except Exception as e:
        logger.warning(f"Could not validate file size for {file_path}: {e}")
        return False


def get_supported_files(input_dir: Path) -> List[Path]:
    """Get list of supported image files from input directory."""
    supported_files = []
    
    for file_path in input_dir.rglob('*'):
        if file_path.is_file() and Config.is_supported_format(str(file_path)):
            if validate_file_size(file_path):
                supported_files.append(file_path)
            else:
                logger.warning(f"Skipping {file_path} due to size limit")
    
    return supported_files 