# API Reference

This document provides a comprehensive reference for all available API endpoints. Each endpoint includes its HTTP method, URL pattern, required parameters, and response format.

## Base URL

All API requests should be made to `https://api.example.com/v2/`. Authentication is required for all endpoints except the health check.

## Rate Limiting

The API enforces rate limits of 100 requests per minute per API key. Exceeding this limit results in a 429 status code with a Retry-After header.
