export function generateReport(results) {
  const errorEntries = results.filter(entry => entry.error === true);
  const successEntries = results.filter(entry => entry.status === 'success');

  return {
    processed_count: successEntries.length,
    error_count: errorEntries.length,
    total_files: results.length,
    errors: errorEntries.map(entry => ({
      file: entry.file,
      message: entry.message,
      details: entry.details
    })),
    results: results
  };
}
