import os
import shutil
from pathlib import Path
from typing import Set


class Config:
    """Configuration management for the Backblaze B2 Image Uploader."""
    
    # CLI Tool Paths
    B2_CLI = shutil.which("b2")
    OP_CLI = shutil.which("op")
    
    # 1Password Settings
    OP_ITEM_NAME = "B2 Application Key Fal"
    
    # B2 Settings  
    BUCKET_NAME = "fal-bucket"
    
    # Directory Settings
    INPUT_DIR = "01.input"
    OUTPUT_DIR = "02.output" 
    DONE_DIR = "03.done"
    
    # Processing Settings
    SUPPORTED_FORMATS: Set[str] = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    SYNC_THREADS = int(os.getenv('SYNC_THREADS', '10'))
    RETRY_ATTEMPTS = int(os.getenv('RETRY_ATTEMPTS', '3'))
    
    # CLI Output Parsing
    URL_PATTERN = r'URL by file name: (https://[^\s]+)'
    SYNC_TIMEOUT = 1800  # 30 minutes for full sync
    
    # File Size Limits
    MAX_FILE_SIZE = 5 * 1024 * 1024 * 1024  # 5GB (B2 limit)
    
    @classmethod
    def get_input_path(cls) -> Path:
        """Get the input directory path."""
        return Path(cls.INPUT_DIR)
    
    @classmethod
    def get_output_path(cls) -> Path:
        """Get the output directory path."""
        return Path(cls.OUTPUT_DIR)
    
    @classmethod
    def get_done_path(cls) -> Path:
        """Get the done directory path."""
        return Path(cls.DONE_DIR)
    
    @classmethod
    def validate_environment(cls) -> bool:
        """Validate that required tools and directories are available."""
        errors = []
        
        # Check CLI tools
        if not cls.B2_CLI:
            errors.append("B2 CLI tool not found in PATH. Please install it first.")
        
        if not cls.OP_CLI:
            errors.append("1Password CLI tool not found in PATH. Please install it first.")
        
        # Check directories
        if not cls.get_input_path().exists():
            errors.append(f"Input directory '{cls.INPUT_DIR}' does not exist.")
        
        # Create output directory if it doesn't exist
        cls.get_output_path().mkdir(exist_ok=True)
        
        if errors:
            print("Environment validation failed:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def is_supported_format(cls, file_path: str) -> bool:
        """Check if a file has a supported image format."""
        return Path(file_path).suffix.lower() in cls.SUPPORTED_FORMATS 