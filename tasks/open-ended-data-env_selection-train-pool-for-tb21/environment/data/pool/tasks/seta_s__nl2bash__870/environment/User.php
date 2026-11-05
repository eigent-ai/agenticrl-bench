<?php

namespace App\Models;

class User
{
    protected $table = 'users';

    protected $fillable = [
        'name',
        'email',
        'password',
        'role',
        'avatar',
        'bio',
        'last_login_at',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'last_login_at' => 'datetime',
        'is_active' => 'boolean',
    ];

    private $attributes = [];
    private $original = [];
    private $relations = [];

    public function __construct(array $attributes = [])
    {
        $this->fill($attributes);
    }
    public function fill(array $attributes)
    {
        foreach ($attributes as $key => $value) {
            if (in_array($key, $this->fillable)) {
                $this->attributes[$key] = $value;
            }
        }
        return $this;
    }
    public function getAttribute($key)
    {
        if (array_key_exists($key, $this->attributes)) {
            return $this->attributes[$key];
        }
        return null;
    }
    public function setAttribute($key, $value)
    {
        $this->attributes[$key] = $value;
        return $this;
    }
    public function posts()
    {
        return $this->hasMany(Post::class, 'user_id');
    }
    public function comments()
    {
        return $this->hasMany('Comment', 'user_id');
    }
    public function profile()
    {
        return $this->hasOne('Profile', 'user_id');
    }
    public function getFullNameAttribute()
    {
        $first = $this->getAttribute('first_name') ?? '';
        $last = $this->getAttribute('last_name') ?? '';
        return trim("{$first} {$last}");
    }
    public function isAdmin()
    {
        return $this->getAttribute('role') === 'admin';
    }
    public function isActive()
    {
        return (bool) $this->getAttribute('is_active');
    }
    public function setPasswordAttribute($value)
    {
        $this->attributes['password'] = password_hash($value, PASSWORD_BCRYPT);
    }
    public function verifyPassword($password)
    {
        return password_verify($password, $this->getAttribute('password'));
    }
    public function toArray()
    {
        $result = [];
        foreach ($this->attributes as $key => $value) {
            if (!in_array($key, $this->hidden)) {
                $result[$key] = $value;
            }
        }
        return $result;
    }
    public static function create(array $attributes)
    {
        $instance = new static($attributes);
        return $instance;
    }
    public static function findOrFail($id)
    {
        return new static(['id' => $id]);
    }
    public function delete()
    {
        return true;
    }
    private function hasMany($class, $foreignKey)
    {
        return [];
    }
}
