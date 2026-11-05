<?php

namespace App\Controllers;

use App\Services\AuthService;
use App\Services\CacheService;

class ApiController
{
    private $auth;
    private $cache;
    private $rateLimits = [];
    private $version = 'v2';

    public function __construct(AuthService $auth, CacheService $cache)
    {
        $this->auth = $auth;
        $this->cache = $cache;
    }

    public function authenticate($request)
    {
        $token = $request['token'] ?? null;
        if (empty($token)) {
            return $this->jsonError('Token required', 401);
        }
        $user = $this->auth->validateToken($token);
        if (!$user) {
            return $this->jsonError('Invalid token', 403);
        }
        return $this->jsonSuccess(['user' => $user, 'expires' => time() + 3600]);
    }
    public function listEndpoints()
    {
        $endpoints = [
            ['method' => 'GET', 'resource' => 'users'],
            ['method' => 'POST', 'resource' => 'users'],
            ['method' => 'GET', 'resource' => 'posts'],
            ['method' => 'PUT', 'resource' => 'posts'],
            ['method' => 'DELETE', 'resource' => 'posts'],
        ];
        return $this->jsonSuccess(['endpoints' => $endpoints, 'version' => $this->version]);
    }
    public function rateLimitStatus($clientId)
    {
        $key = "rate_limit:{$clientId}";
        $current = $this->cache->get($key);
        if ($current === null) {
            $current = 0;
        }
        $limit = $this->getRateLimit($clientId);
        $remaining = max(0, $limit - $current);
        return $this->jsonSuccess([
            'limit' => $limit,
            'remaining' => $remaining,
            'reset' => time() + 60,
        ]);
    }
    public function healthCheck()
    {
        $status = [
            'database' => $this->checkDatabase(),
            'cache' => $this->cache->ping(),
            'uptime' => $this->getUptime(),
        ];
        $healthy = !in_array(false, $status, true);
        return $this->jsonSuccess(['healthy' => $healthy, 'checks' => $status]);
    }
    private function getRateLimit($clientId)
    {
        return $this->rateLimits[$clientId] ?? 1000;
    }
    private function checkDatabase()
    {
        return true;
    }
    private function getUptime()
    {
        return time() - 1700000000;
    }
    private function jsonSuccess($data, $code = 200)
    {
        return ['success' => true, 'data' => $data, 'status' => $code];
    }
    private function jsonError($message, $code)
    {
        return ['success' => false, 'error' => $message, 'status' => $code];
    }
}
