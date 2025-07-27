# Backblaze B2 Image Uploader

A Python script that uploads images from a local input directory to a Backblaze B2 bucket, providing comprehensive logging and link generation. The script follows the standardized input/output pattern and uses 1Password CLI for secure authentication.

## Features

- **Folder Mirroring**: Mirror `01.input/` folder to Backblaze B2 bucket using `b2 sync`
- **Automatic Sync**: Keep local folder and B2 bucket in sync with any changes
- **Link Generation**: Generate friendly public links for all synced images
- **Comprehensive Logging**: Machine-readable logs and human-readable failure reports
- **Secure Authentication**: Uses 1Password CLI for secure credential management
- **Dry Run Support**: Preview changes before making them
- **Clean Operations**: Safely remove all files from bucket with confirmation

## Directory Structure

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

## Prerequisites

### System Requirements
- Python 3.8+
- **Backblaze B2 CLI** (`b2`) installed and available in PATH
- **1Password CLI** (`op`) installed and configured
- Internet connection for B2 operations

### 1Password Setup
You need a 1Password item named "Backblaze Application Key Cyberduck" with the following fields:
- `keyID`: Your B2 Application Key ID
- `keyName`: Your B2 Application Key Name  
- `Bucket`: Target bucket name (should be "fal-bucket")
- `applicationKey`: Your B2 Application Key

## Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up 1Password CLI**:
   ```bash
   op signin
   ```
4. **Create required directories**:
   ```bash
   mkdir -p 01.input 02.output 03.done
   ```
5. **Copy environment template** (optional):
   ```bash
   cp .env.example .env
   ```

## Usage

### Basic Sync (Default Operation)
```bash
# Sync files from 01.input/ to B2 bucket
python b2_uploader.py

# Explicit sync command
python b2_uploader.py sync
```

### Preview Changes (Dry Run)
```bash
# Preview what would be synced without making changes
python b2_uploader.py sync --dry-run
```

### Clean Bucket
```bash
# Remove all files from bucket (with confirmation)
python b2_uploader.py clean

# Remove all files without confirmation
python b2_uploader.py clean --force

# Preview what would be deleted
python b2_uploader.py clean --dry-run
```

### Verbose Logging
```bash
# Enable detailed logging
python b2_uploader.py sync --verbose
```

## Configuration

### Environment Variables
Create a `.env` file with the following variables (optional):
```bash
SYNC_THREADS=10
RETRY_ATTEMPTS=3
```

### Supported Image Formats
The script supports these image formats:
- `.jpg`, `.jpeg`
- `.png`
- `.gif`
- `.bmp`
- `.tiff`
- `.webp`

### File Size Limits
- Maximum file size: 5GB (B2 limit)

## Output Files

### JSON Log File
**Filename**: `YYYYMMDD_HHMMSS_sync_log.json`
Contains comprehensive machine-readable logging data including:
- Run metadata (timestamp, operation, file counts)
- Detailed file processing information
- Error reports
- Execution timing

### Link File
**Filename**: `YYYYMMDD_HHMMSS_bucket-links.txt`
Human-readable list of public URLs for all synced files.

### Failure Report
**Filename**: `FAILURE.md` (only created if errors occur)
Human-readable error summary with troubleshooting steps.

## Error Handling

The script includes comprehensive error handling for:
- **Authentication Errors**: Invalid 1Password session, missing credentials
- **B2 CLI Errors**: Network failures, permission issues, quota exceeded
- **File Errors**: Invalid formats, size limits, corruption
- **System Errors**: Missing tools, permission issues, disk space

## Security

- **Credential Management**: Never stores B2 credentials in code or config files
- **1Password Integration**: Uses 1Password CLI for secure credential retrieval
- **Memory Safety**: Clears credentials from memory after use
- **File Validation**: Validates file paths and types before processing

## Troubleshooting

### Common Issues

**1Password CLI not found**
```bash
# Install 1Password CLI
# macOS: brew install 1password-cli
# Linux: Follow official installation guide
```

**B2 CLI not found**
```bash
# Install B2 CLI
# macOS: brew install b2-tools
# Linux: Download from Backblaze website
```

**Authentication failed**
```bash
# Check 1Password session
op account list

# Sign in if needed
op signin
```

**Bucket not found**
- Verify the bucket name in your 1Password item
- Ensure your B2 account has access to the bucket

## Development

### Project Structure
- `b2_uploader.py`: Main CLI interface and orchestration
- `config.py`: Configuration management and validation
- `b2_auth.py`: 1Password and B2 authentication
- `utils.py`: Utility functions for logging and file operations

### Testing
```bash
# Test help
python b2_uploader.py --help

# Test dry run
python b2_uploader.py sync --dry-run

# Test clean preview
python b2_uploader.py clean --dry-run
```

## License

This project is provided as-is for educational and development purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the generated log files in `02.output/`
3. Ensure all prerequisites are properly installed and configured 