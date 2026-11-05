<?php

namespace App\Services;

class CacheService
{
    private $store = [];
    private $defaultTtl = 3600;
    private $prefix = 'app_';
    private $hits = 0;
    private $misses = 0;

    public function get($key, $default = null)
    {
        $prefixedKey = $this->prefix . $key;
        if (!isset($this->store[$prefixedKey])) {
            $this->misses++;
            return $default;
        }
        $item = $this->store[$prefixedKey];
        if ($item['expires_at'] !== null && $item['expires_at'] < time()) {
            unset($this->store[$prefixedKey]);
            $this->misses++;
            return $default;
        }
        $this->hits++;
        return $item['value'];
    }
    public function put($key, $value, $ttl = null)
    {
        $prefixedKey = $this->prefix . $key;
        $expiresAt = ($ttl !== null) ? time() + $ttl : time() + $this->defaultTtl;
        $this->store[$prefixedKey] = [
            'value' => $value,
            'created_at' => time(),
            'expires_at' => $expiresAt,
        ];
        return true;
    }
    public function forget($key)
    {
        $prefixedKey = $this->prefix . $key;
        if (isset($this->store[$prefixedKey])) {
            unset($this->store[$prefixedKey]);
            return true;
        }
        return false;
    }
    public function has($key)
    {
        return $this->get($key) !== null;
    }
    public function flush()
    {
        $this->store = [];
        $this->hits = 0;
        $this->misses = 0;
        return true;
    }
    public function remember($key, $ttl, $callback)
    {
        $value = $this->get($key);
        if ($value !== null) {
            return $value;
        }
        $value = $callback();
        $this->put($key, $value, $ttl);
        return $value;
    }
    public function increment($key, $amount = 1)
    {
        $current = $this->get($key, 0);
        $newValue = $current + $amount;
        $this->put($key, $newValue);
        return $newValue;
    }
    public function decrement($key, $amount = 1)
    {
        return $this->increment($key, -$amount);
    }
    public function getStats()
    {
        $total = $this->hits + $this->misses;
        return [
            'hits' => $this->hits,
            'misses' => $this->misses,
            'ratio' => $total > 0 ? $this->hits / $total : 0,
            'size' => count($this->store),
        ];
    }
    public function ping()
    {
        return true;
    }
}
