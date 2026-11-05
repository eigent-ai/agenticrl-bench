# Changelog - {{date}}

All notable changes to DocForge are documented here.

## Version 0.1.0

Release date: {{date}}

### Added

- Initial ECS-inspired pipeline architecture
- Font normalization plugin with configurable default font
- Template variable expansion for dates and filenames
- Cross-reference resolution between documents
- Table of contents generation for multi-heading documents
- Manifest generation with document metadata

### Known Issues

- Pipeline may short-circuit if a stage returns empty results
- Font configuration defaults may not be properly initialized

## Roadmap

Future versions will include:

- PDF output support
- Custom plugin API
- Incremental processing
- Watch mode for live rebuilds

For contributing guidelines, see [[contributing.md]].
For architecture details, see [[architecture.md]].
