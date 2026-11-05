# Frequently Asked Questions

Common questions and answers about DocForge.

## General

### What file formats does DocForge support?

DocForge currently supports Markdown input files and produces HTML output.

### Can I customize the output format?

Yes, through the plugin architecture. See [[architecture.md]] for details on
creating custom plugins.

## Troubleshooting

### Why are my output files empty?

Check that the pipeline is running all stages. Enable debug logging:

```bash
RUST_LOG=debug docforge process --input docs/ --output build/
```

### Why is font normalization not working?

Ensure the `FontConfig` resource has a valid font family name. The default
configuration should use "Inter" as the standard font.

### How do cross-references work?

Wrap a document filename in double brackets to create an automatic link to
that document. These are resolved to HTML anchor tags during processing.

## Performance

### How fast is the pipeline?

Processing time depends on document count and complexity. For 100 documents,
expect sub-second processing time on modern hardware.

For more help, see the [[guide.md]] or consult the [[api.md]].
