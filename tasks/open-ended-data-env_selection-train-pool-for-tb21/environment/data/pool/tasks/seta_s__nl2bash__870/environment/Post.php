<?php

namespace App\Models;

class Post
{
    protected $table = 'posts';

    protected $fillable = [
        'title',
        'slug',
        'body',
        'excerpt',
        'status',
        'published_at',
        'user_id',
    ];

    protected $casts = [
        'published_at' => 'datetime',
        'is_featured' => 'boolean',
    ];

    private $attributes = [];

    public function __construct(array $attributes = [])
    {
        foreach ($attributes as $key => $value) {
            if (in_array($key, $this->fillable)) {
                $this->attributes[$key] = $value;
            }
        }
    }

    public function author()
    {
        return new User(['id' => $this->attributes['user_id'] ?? 0]);
    }
    public function comments()
    {
        return [];
    }
    public function tags()
    {
        return [];
    }
    public function isPublished()
    {
        return ($this->attributes['status'] ?? '') === 'published';
    }
    public function isDraft()
    {
        return ($this->attributes['status'] ?? 'draft') === 'draft';
    }
    public function getExcerpt($length = 150)
    {
        $body = $this->attributes['body'] ?? '';
        if (strlen($body) <= $length) {
            return $body;
        }
        return substr($body, 0, $length) . '...';
    }
    public function generateSlug()
    {
        $title = $this->attributes['title'] ?? '';
        $slug = strtolower(trim(preg_replace('/[^A-Za-z0-9-]+/', '-', $title), '-'));
        $this->attributes['slug'] = $slug;
        return $slug;
    }
    public function toArray()
    {
        return $this->attributes;
    }
    public static function paginate($perPage = 15)
    {
        return [];
    }
}
