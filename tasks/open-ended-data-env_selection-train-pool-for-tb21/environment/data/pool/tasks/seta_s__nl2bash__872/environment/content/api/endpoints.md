# API Endpoints

Complete reference of all REST API endpoints organized by resource type.

## Users

- `GET /api/v2/users` - List all users (paginated)
- `GET /api/v2/users/:id` - Get a specific user
- `POST /api/v2/users` - Create a new user
- `PATCH /api/v2/users/:id` - Update user attributes
- `DELETE /api/v2/users/:id` - Deactivate a user

## Projects

- `GET /api/v2/projects` - List all projects for the authenticated user
- `POST /api/v2/projects` - Create a new project
- `GET /api/v2/projects/:id` - Get project details including statistics
- `PUT /api/v2/projects/:id` - Replace project configuration

## Webhooks

- `GET /api/v2/webhooks` - List configured webhooks
- `POST /api/v2/webhooks` - Register a new webhook endpoint
