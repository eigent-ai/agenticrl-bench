<?php

namespace App\Controllers;

use App\Models\User;
use App\Services\AuthService;

class UserController
{
    private $authService;
    private $perPage = 20;

    public function __construct(AuthService $auth)
    {
        $this->authService = $auth;
    }

    public function index()
    {
        $users = User::paginate($this->perPage);
        return $this->respond('users.index', ['users' => $users]);
    }

    public function show($id)
    {
        $user = User::findOrFail($id);
        if (!$user) {
            return $this->errorResponse('User not found', 404);
        }
        return $this->respond('users.show', ['user' => $user]);
    }

    public function store($request)
    {
        $validated = $this->validate($request, [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8',
        ]);
        $user = User::create($validated);
        return $this->respond('users.show', ['user' => $user], 201);
    }

    public function update($id, $request)
    {
        $user = User::findOrFail($id);
        $user->update($request);
        return $this->respond('users.show', ['user' => $user]);
    }

    public function destroy($id)
    {
        $user = User::findOrFail($id);
        $user->delete();
        return $this->respond('users.deleted', [], 204);
    }

    private function respond($view, $data, $code = 200)
    {
        return ['view' => $view, 'data' => $data, 'status' => $code];
    }
}
