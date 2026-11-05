# Project Documentation

## Overview

This project provides a multi-language data processing pipeline that handles
file classification, image metadata extraction, and batch processing operations.

## Architecture

The project is structured as follows:

- `src/main/java/` — Core Java application (file processing, classification)
- `src/main/python/` — Python utilities and processing pipeline
- `src/main/resources/` — Configuration and template files
- `src/test/` — Test files for both Java and Python components
- `scripts/` — Build and deployment automation

## Building

```bash
make build
```

## Running Tests

```bash
make test
```

## Deployment

```bash
bash scripts/deploy.sh [staging|production]
```

## Distribution

To generate a source distribution manifest:

```bash
bash scripts/generate_manifest.sh
```

This creates `MANIFEST.txt` listing all distributable source files.
