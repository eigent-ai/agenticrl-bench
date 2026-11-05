function sanitizeHtml(input) {
  let clean = input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  return clean;
}

function validateComment(body) {
  const errors = [];

  if (!body.content || typeof body.content !== 'string' || body.content.trim().length === 0) {
    errors.push({ field: 'content', message: 'Comment content is required' });
  }

  if (body.content && body.content.length > 10000) {
    errors.push({ field: 'content', message: 'Comment content exceeds maximum length of 10000 characters' });
  }

  if (!body.userId) {
    errors.push({ field: 'userId', message: 'User ID is required' });
  }

  return errors;
}

module.exports = { validateComment, sanitizeHtml };
