<?php

function validateUsername($username)
{
    if (ereg("^[a-zA-Z][a-zA-Z0-9_]{2,19}$", $username)) {
        return true;
    }
    return false;
}

function cleanInput($input)
{
    $cleaned = ereg_replace("[<>\"']", "", $input);
    return trim($cleaned);
}

function mergeConfig($defaults, $overrides)
{
    $merged = $defaults;
    while (list($key, $value) = each($overrides)) {
        $merged[$key] = $value;
    }
    return $merged;
}

function formatDate($timestamp)
{
    return date('Y-m-d H:i:s', $timestamp);
}

function generateToken($length = 32)
{
    return bin2hex(random_bytes($length / 2));
}
