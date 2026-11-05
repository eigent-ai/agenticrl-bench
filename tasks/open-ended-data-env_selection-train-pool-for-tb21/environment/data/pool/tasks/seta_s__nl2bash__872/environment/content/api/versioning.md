# API Versioning

The API uses URL-based versioning. The current stable version is v2. Version v1 is deprecated and will be removed on December 31, 2025.

## Version Lifecycle

Each API version follows a defined lifecycle: Preview (6 months), Stable (minimum 2 years), Deprecated (6 months notice), and Retired.

## Migration Guide

To migrate from v1 to v2, update your base URL from `/api/v1/` to `/api/v2/` and review the breaking changes listed in the changelog. Key changes include pagination format (cursor-based instead of offset) and date fields (ISO 8601 instead of Unix timestamps).

## Changelog

All API changes are documented in the changelog, available at `/api/changelog`. Subscribe to the API announcements mailing list for advance notice of breaking changes.
