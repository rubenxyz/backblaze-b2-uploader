# Backblaze B2 Image Uploader - Product Requirements Document

## Overview
A Python script that uploads images from a local input directory to a Backblaze B2 bucket, providing comprehensive logging and link generation. The script follows the standardized input/output pattern and uses 1Password CLI for secure authentication.

## Core Functionality

### Primary Features
1. **Image Upload**: Batch upload all images from `01.input/` to Backblaze B2
2. **Bucket Management**: Complete bucket wipe functionality for cleanup
3. **Link Generation**: Generate friendly public links for all uploaded images
4. **Comprehensive Logging**: Machine-readable logs and human-readable failure reports

## Directory Structure

### Standard Folder Structure
```
backblaze-uploader/
├── b2_uploader.py              # Main script entry point
├── config.py                   # Configuration management
├── b2_auth.py                  # 1Password + B2 authentication
├── utils.py                    # Utility functions
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
├── .env.example               # Environment template
├── .gitignore                 # Excludes input/output dirs
├── 00.ready/                  # Staging area (ignored by script)
├── 01.input/                  # Images to upload (processed by script)
├── 02.output/                 # Results and logs (timestamped folders)
└── 03.done/                   # Processed images (ignored by script)
```

### Input Directory (`01.input/`)
- Contains all image files to be uploaded to B2
- Supports common image formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
- Maintains subdirectory structure for organized uploads
- Script processes all images recursively

### Output Directory (`02.output/`)
- Creates timestamped subdirectories: `YYYYMMDD_HHMMSS/`
- Contains processing results for each run:
  - Verbose log file (machine-readable, LLM-optimized)
  - Link list file with public URLs
  - Human-readable failure report (if errors occur)

## Authentication Requirements

### 1Password CLI Integration
- **Item Name**: "Backblaze Application Key Cyberduck"
- **Required Fields**:
  - `keyID`: B2 Application Key ID
  - `keyName`: B2 Application Key Name  
  - `Bucket`: Target bucket name (should be "fal-bucket")
  - `applicationKey`: B2 Application Key

### Authentication Flow
1. Check if 1Password CLI session is active
2. If expired, trigger interactive sign-in
3. Retrieve B2 credentials from specified 1Password item
4. Use `b2 account authorize` CLI command with retrieved credentials
5. Verify authentication with `b2 account get` command

## Core Operations

### Upload Mode (Default)
**Command**: `python b2_uploader.py upload` or `python b2_uploader.py`

**Process Flow**:
1. Initialize logging and configuration
2. Authenticate with 1Password and retrieve B2 credentials
3. Authorize B2 CLI using `b2 account authorize <keyID> <applicationKey>`
4. Scan `01.input/` for image files recursively
5. Create timestamped output directory
6. For each image file:
   - Upload using `b2 file upload fal-bucket <local_file> <remote_path>`
   - Parse CLI output to extract public URL
   - Log upload result with timing and file size
7. Generate comprehensive logs and `bucket-links.txt` file
8. Move processed images to `03.done/` (optional)

**CLI Commands Used**:
- `b2 account authorize <keyID> <applicationKey>` - Authenticate with B2
- `b2 file upload fal-bucket <local_file> <remote_name>` - Upload individual files
- `b2 account get` - Verify authentication status

**Error Handling**:
- Continue processing on individual file failures
- Parse CLI error messages for detailed context
- Generate `FAILURE.md` for any failures encountered
- Provide recovery options for partial uploads

### Wipe Mode
**Command**: `python b2_uploader.py wipe`

**Process Flow**:
1. Authenticate with 1Password and B2 CLI
2. Verify bucket exists using `b2 bucket list`
3. List current files using `b2 ls --long b2://fal-bucket`
4. Confirm deletion with user prompt (show file count)
5. Execute `b2 rm --versions --recursive b2://fal-bucket` to delete all files
6. Clean up any unfinished large files with `b2 cancel-all-unfinished-large-files fal-bucket`
7. Log deletion results with file counts and timing

**CLI Commands Used**:
- `b2 bucket list` - Verify bucket exists
- `b2 ls --long b2://fal-bucket` - List files for confirmation
- `b2 rm --versions --recursive b2://fal-bucket` - Delete all files and versions
- `b2 cancel-all-unfinished-large-files fal-bucket` - Clean up incomplete uploads

**Safety Features**:
- Interactive confirmation before deletion (shows file count)
- `--force` flag to skip confirmation
- Detailed logging of deleted files with counts
- Warning about permanent operation

## Output Files

### Log File (Machine-Readable)
**Filename**: `YYYYMMDD_HHMMSS_upload_log.json`
**Purpose**: Comprehensive logging for LLM analysis
**Content**:
```json
{
  "run_metadata": {
    "timestamp": "2025-07-27T15:30:45",
    "operation": "upload",
    "total_files": 25,
    "successful_uploads": 23,
    "failed_uploads": 2,
    "execution_time_seconds": 45.7
  },
  "files_processed": [
    {
      "local_path": "01.input/photos/IMG_001.jpg",
      "b2_key": "photos/IMG_001.jpg",
      "public_url": "https://f001.backblazeb2.com/file/fal-bucket/photos/IMG_001.jpg",
      "upload_time": "2025-07-27T15:30:47",
      "file_size_bytes": 2048576,
      "status": "success"
    }
  ],
  "errors": [
    {
      "file": "01.input/corrupted.jpg",
      "error_type": "InvalidImageFormat",
      "error_message": "File is corrupted or not a valid image",
      "timestamp": "2025-07-27T15:30:52"
    }
  ]
}
```

### Link File
**Filename**: `YYYYMMDD_HHMMSS_bucket-links.txt`
**Purpose**: Human-readable list of public URLs
**Format**:
```
# Backblaze B2 Upload Links - 2025-07-27 15:30:45
# Bucket: fal-bucket
# Total Files: 23

photos/IMG_001.jpg
https://f001.backblazeb2.com/file/fal-bucket/photos/IMG_001.jpg

photos/IMG_002.jpg  
https://f001.backblazeb2.com/file/fal-bucket/photos/IMG_002.jpg
```

### Failure Report (Human-Readable)
**Filename**: `FAILURE.md` (only created if errors occur)
**Purpose**: Human-readable error summary
**Content**:
```markdown
# Upload Failure Report
**Date**: 2025-07-27 15:30:45
**Operation**: Image Upload to fal-bucket

## Summary
- **Total Files**: 25
- **Successful**: 23  
- **Failed**: 2

## Failed Files
### corrupted.jpg
- **Error**: File is corrupted or not a valid image
- **Solution**: Check file integrity and format

### large_image.png
- **Error**: File size exceeds 5GB limit
- **Solution**: Compress image or split into smaller files

## Next Steps
1. Fix the identified issues with failed files
2. Move failed files to 00.ready/ for retry
3. Re-run the upload script
```

## Configuration

### Hardcoded Settings
- **Bucket Name**: `fal-bucket` (not configurable)
- **Supported Formats**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`
- **Max File Size**: 5GB (B2 limit)

### Environment Configuration
```python
# config.py
import os
import shutil

class Config:
    # CLI Tool Paths
    B2_CLI = shutil.which("b2")
    OP_CLI = shutil.which("op")
    
    # 1Password Settings
    OP_ITEM_NAME = "Backblaze Application Key Cyberduck"
    
    # B2 Settings  
    BUCKET_NAME = "fal-bucket"
    
    # Directory Settings
    INPUT_DIR = "01.input"
    OUTPUT_DIR = "02.output" 
    DONE_DIR = "03.done"
    
    # Processing Settings
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    MAX_PARALLEL_UPLOADS = int(os.getenv('MAX_PARALLEL_UPLOADS', '4'))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    
    # CLI Output Parsing
    URL_PATTERN = r'URL by file name: (https://[^\s]+)'
    UPLOAD_TIMEOUT = 300  # 5 minutes per file
```

## Command-Line Interface

### Usage Examples
```bash
# Upload all images (default mode)
python b2_uploader.py

# Upload with explicit command
python b2_uploader.py upload

# Wipe all files from bucket (with confirmation)
python b2_uploader.py wipe

# Wipe bucket without confirmation
python b2_uploader.py wipe --force

# Upload with custom parallel workers
MAX_PARALLEL_UPLOADS=8 python b2_uploader.py upload
```

### Arguments
- `operation`: `upload` (default) or `wipe`
- `--force`: Skip confirmation prompts (wipe mode only)
- `--dry-run`: Simulate operations without actual uploads/deletions
- `--verbose`: Enable debug-level console logging

## Dependencies

### Required Libraries
```txt
# requirements.txt
loguru>=0.7.0
click>=8.1.0
pathlib>=1.0.1
python-dotenv>=1.0.0
```

### System Requirements
- Python 3.8+
- **Backblaze B2 CLI** (`b2`) installed and available in PATH
- **1Password CLI** (`op`) installed and configured
- Internet connection for B2 operations
- Sufficient disk space for temporary files

## Error Handling

### Authentication Errors
- Invalid 1Password session → Trigger interactive sign-in
- Missing B2 credentials in 1Password → Clear error message with setup instructions
- Invalid B2 keys → B2 CLI authentication failure with troubleshooting steps
- B2 CLI not found → Installation instructions and requirements check

### Upload Errors  
- B2 CLI network failures → Retry with exponential backoff
- File format validation → Pre-validate before CLI upload
- Bucket permission errors → Parse CLI error and provide clear guidance
- File size exceeded → CLI will report size limit, skip with explanation
- CLI timeout → Handle long uploads with extended timeout values

### CLI-Specific Errors
- **Return Code 1**: Authentication failure or invalid credentials
- **Return Code 2**: File not found or permission denied
- **Network Errors**: Parse CLI stderr for connection issues
- **Quota Exceeded**: Parse CLI output for storage limit messages
- **Invalid Bucket**: CLI reports bucket access or existence issues

### System Errors
- Missing input directory → Create directory and provide instructions
- B2 CLI not in PATH → Installation and setup guidance
- Permission issues → Detailed error with resolution steps
- Disk space → Monitor during large uploads and provide warnings

## Security Considerations

### Credential Management
- Never store B2 credentials in code or config files
- Use 1Password CLI for secure credential retrieval
- Clear credentials from memory after use
- Log authentication events without exposing secrets

### File Safety
- Validate file paths to prevent directory traversal
- Sanitize filenames for B2 compatibility
- Check file types against allowed formats
- Implement file size limits

## Performance Requirements

### Upload Performance
- **Parallel Uploads**: 4 concurrent uploads (configurable)
- **Progress Reporting**: Real-time progress for large operations
- **Memory Management**: Stream large files to avoid memory issues
- **Network Optimization**: Retry failed uploads with backoff

### Resource Management
- **CPU Usage**: Moderate during concurrent uploads
- **Memory Usage**: < 500MB for typical operations
- **Disk Space**: Minimal temporary storage required
- **Network**: Bandwidth-dependent, respects B2 rate limits

## Testing Strategy

### Unit Tests
- Authentication flow with mocked 1Password responses
- File validation and filtering logic
- Error handling for various failure scenarios
- Configuration loading and validation

### Integration Tests
- End-to-end upload workflow with test bucket
- 1Password CLI integration with test credentials
- Link generation and validation
- Cleanup and recovery operations

### Manual Testing
- Large file uploads (approaching 5GB limit)
- Network interruption recovery
- Bucket wipe confirmation flow
- Error reporting accuracy

## Future Enhancements

### Potential Features
- **Resume Capability**: Resume interrupted uploads
- **Compression**: Optional image compression before upload
- **Metadata Preservation**: Maintain EXIF data and timestamps
- **Folder Mirroring**: Sync local changes to bucket
- **CDN Integration**: Generate CDN URLs for faster access

### Scalability Considerations
- Support for multiple buckets
- Configuration file for advanced settings
- Plugin system for custom processors
- Web interface for non-technical users