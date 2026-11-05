function validateProfile(body) {
  const errors = [];

  if (body.displayName !== undefined) {
    if (typeof body.displayName !== 'string' || body.displayName.trim().length === 0) {
      errors.push({ field: 'displayName', message: 'Display name cannot be empty' });
    }
    if (typeof body.displayName === 'string' && body.displayName.length > 100) {
      errors.push({ field: 'displayName', message: 'Display name is too long' });
    }
  }

  if (body.bio !== undefined) {
    if (typeof body.bio !== 'string') {
      errors.push({ field: 'bio', message: 'Bio must be a string' });
    } else if (body.bio.length > 500) {
      errors.push({ field: 'bio', message: 'Bio is too long (max 500 characters)' });
    }
  }

  if (body.website !== undefined && body.website !== '') {
    const urlRegex = /^https?:\/\/.*\..+$/;
    if (!urlRegex.test(body.website)) {
      errors.push({ field: 'website', message: 'Website must be a valid HTTP/HTTPS URL' });
    }
  }

  if (!body.userId) {
    errors.push({ field: 'userId', message: 'User ID is required' });
  }

  return errors;
}

module.exports = { validateProfile };
