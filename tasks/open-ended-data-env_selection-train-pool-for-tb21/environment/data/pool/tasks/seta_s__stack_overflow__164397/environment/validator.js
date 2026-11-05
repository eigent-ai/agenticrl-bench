const REQUIRED_FIELDS = ['id', 'name', 'value'];

export function validate(data, fileName) {
  if (typeof data !== 'object' || data === null) {
    const err = new Error(`Invalid data format in ${fileName}`);
    err.details = { field: null, reason: 'not an object', file: fileName };
    throw err;
  }

  for (const field of REQUIRED_FIELDS) {
    if (!(field in data) || data[field] === undefined || data[field] === null) {
      const err = new Error(`Missing required field '${field}' in ${fileName}`);
      err.details = { field: field, reason: 'missing', file: fileName };
      throw err;
    }
  }

  return true;
}
