# Architecture Overview

## Component Diagram

```
┌─────────────────┐     ┌──────────────────┐
│   Main.java     │────▶│ ImageProcessor   │
│   (entry point) │     │ (file handling)  │
└────────┬────────┘     └──────────────────┘
         │
         ▼
┌─────────────────┐     ┌──────────────────┐
│  Reclassifier   │────▶│  Utils.java      │
│  (categorizer)  │     │  (shared utils)  │
└─────────────────┘     └──────────────────┘
```

## Python Pipeline

```
helpers.py ──▶ processor.py ──▶ png_utils.py
(file I/O)    (orchestrator)   (PNG metadata)
```

## Data Flow

1. Main.java receives input directory path
2. ImageProcessor handles binary file detection
3. Reclassifier categorizes files by extension/content
4. Python pipeline performs batch processing
5. Results written to output directory as JSON reports

## Key Design Decisions

- Separation between Java (core processing) and Python (utilities/scripting)
- File-based communication between components
- Extension-based classification with fallback heuristics
- Streaming file reads for memory efficiency
