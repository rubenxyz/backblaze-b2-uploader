# Input/Output Pattern for Batch Processing Projects

## Overview
This document describes a standardized approach for batch processing projects that transform files from an input directory to an output directory while maintaining folder hierarchy and providing comprehensive logging.

## Core Philosophy
The pattern emphasizes simplicity, reproducibility, and transparency. Users place their files in a predictable input location, run the processing tool, and receive organized results in a dedicated output location with detailed logs for both human and machine consumption.

## Directory Structure

### Standard Folder Structure
The batch processing system uses a standardized four-folder structure:

```
project_root/
├── 00.ready/          # Files ready for processing (ignored by script)
├── 01.input/          # Active input folder (script processes this)
├── 02.output/         # Generated output files and folders
└── 03.done/           # Processed input files (ignored by script)
```

### Folder Descriptions

**00.ready/**
- Contains files that are ready to be moved to the input folder
- **Ignored by the processing script** - not processed automatically
- Used as a staging area for files before processing
- Files must be manually moved to `01.input/` to be processed

**01.input/**
- The active input directory that the script processes
- Contains all files and subdirectories to be processed
- Maintains user's organizational structure
- Script reads from this folder exclusively

**02.output/**
- Contains all processed results and generated files
- Organized in timestamped subdirectories (`YYYY-MM-DD_HH-MM-SS`)
- Mirrors the input structure with processed files
- Each processing run creates a new timestamped folder

**03.done/**
- Contains input files that have been processed
- **Ignored by the processing script** - not reprocessed
- Used to archive processed input files
- Files are moved here after successful processing

### Input Directory
The input directory serves as the single source of truth for all files to be processed. Users organize their files in subdirectories according to their own logical structure. The processing tool respects and preserves this organization.

### Output Directory
The output directory contains all processed results, organized in dated timestamped subdirectories down to the seconds, to prevent overwrites and maintain a clear history of processing runs. Each run creates a new timestamped folder that mirrors the input structure but with processed files.

## Processing Modes

### Analysis Mode
When the tool runs in analysis mode, it examines all files in the input directory without making any modifications. It generates comprehensive reports that describe the current state of all files, their properties, and any insights that can be extracted from them.

### Transformation Mode
When the tool runs in transformation mode, it reads configuration from the input directory, processes all files according to the specified parameters, and creates transformed versions in the output directory while maintaining the original folder structure.

## Configuration Management
Configuration files are placed directly in the input subdirectory alongside the folders to be processed. This keeps all related information together and makes it clear which configuration applies to which set of files. The configuration specifies the transformation parameters and processing options.

## Logging Strategy

### Dual Logging Approach
The system generates two types of logs for each processing run:

**Machine-Readable Logs (XML)**
These logs contain detailed, structured information designed for programmatic consumption. They include comprehensive metadata, processing statistics, error details, and technical information that can be parsed and analyzed by other tools or AI systems.

**Human-Readable Logs (Markdown)**
These logs provide a concise, readable summary of the processing run. They focus on high-level outcomes, success/failure status, and any issues that require human attention. The format is designed for quick scanning and understanding.

### Logging Framework
The system uses Loguru for structured logging, providing consistent formatting, log levels, and output handling across all processing operations. Logs are automatically timestamped and organized by processing run.

## File Naming and Organization

### Input Preservation
The original folder structure from the input directory is preserved in the output directory. This maintains the user's organizational logic and makes it easy to locate corresponding processed files.

### Timestamped Outputs
Each processing run creates a new timestamped directory in the output folder using the format `YYYY-MM-DD_HH-MM-SS` (e.g., `2025-07-20_18-59-10`). This prevents accidental overwrites and provides a clear audit trail of all processing operations. The timestamp format is consistent across all processing tools and does not include descriptive prefixes.

### Output Directory Naming Convention
- **Format**: `YYYY-MM-DD_HH-MM-SS` (e.g., `2025-07-20_18-59-10`)
- **No descriptive prefixes**: Avoid names like `batch_`, `processed_`, or `code_blocks_fixed_`
- **Consistency**: All processing tools use the same timestamp-only format
- **Simplicity**: Easy to sort chronologically and identify processing runs

### File Naming Conventions
Processed files maintain their original names but folders may include suffixes or prefixes that indicate the transformation applied. This makes it clear what processing has been done while preserving the original file identity. Output directories use only timestamp format (`YYYY-MM-DD_HH-MM-SS`) without descriptive prefixes to maintain consistency and simplicity.

## Error Handling and Recovery

### Graceful Degradation
The system continues processing even when individual files fail. Failed files are logged with detailed error information, but the overall process continues to completion.

### Clear Error Reporting
Errors are categorized and reported in both the machine-readable and human-readable logs, with appropriate detail levels for each audience.

### Recovery Options
The system provides options to retry failed operations, skip problematic files, or continue from where processing left off in case of interruption.

### Performance
The pattern should be designed to handle large file collections efficiently, with progress reporting and the ability to process files in parallel when appropriate.

## Version Control and Git Ignore Patterns

### Input and Output Directory Exclusion
**Input and output directories should ALWAYS be excluded from version control** by adding them to `.gitignore`. This is a fundamental requirement for all batch processing projects.

### Rationale for Exclusion
1. **Repository Size Management**: Input files may contain large datasets, and output files are generated content that can be very large
2. **Data Privacy**: Input files may contain sensitive or proprietary information that shouldn't be shared
3. **Reproducibility**: Output files are regenerated each time the script runs, so they don't need version control
4. **Focus on Code**: Version control should focus on the processing logic, not the data being processed

### Required .gitignore Entries
Every batch processing project must include these entries in `.gitignore`:
```
# Input and output directories
input/
output/
00.ready/
```

### Alternative Patterns
For projects that need to track some input/output files, use more specific patterns:
```
# Exclude all input/output but allow specific files
input/*
!input/example.tsv
!input/README.md

output/*
!output/.gitkeep
```

### Best Practices
- **Never commit input data** unless it's small, non-sensitive example files
- **Never commit output files** as they are regenerated content
- **Document input format** in README files instead of committing sample data
- **Use .gitkeep files** in empty directories if needed for project structure
- **Include input/output directories** in project documentation so users know where to place files

