# Authentication

All API requests require authentication using either API keys or OAuth 2.0 bearer tokens.

## API Keys

Generate API keys from the dashboard under Settings > API Keys. Include the key in the Authorization header:

```
Authorization: Bearer your-api-key-here
```

API keys have configurable scopes and expiration dates. Rotate keys regularly and never commit them to version control.

## OAuth 2.0

For user-facing applications, use the OAuth 2.0 authorization code flow. Register your application to receive a client ID and secret. The authorization endpoint is `/oauth/authorize` and the token endpoint is `/oauth/token`.

## Token Refresh

Access tokens expire after one hour. Use the refresh token to obtain a new access token without requiring user interaction.
