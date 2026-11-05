<?php

namespace App\Utils;

class StringUtils
{
    public static function camelCase($string)
    {
        $words = explode('_', $string);
        $result = array_shift($words);
        foreach ($words as $word) {
            $result .= ucfirst($word);
        }
        return $result;
    }

    public static function snakeCase($string)
    {
        $result = preg_replace('/[A-Z]/', '_$0', $string);
        return strtolower(ltrim($result, '_'));
    }

    public static function truncate($string, $length = 100, $suffix = '...')
    {
        if (strlen($string) <= $length) {
            return $string;
        }
        return substr($string, 0, $length - strlen($suffix)) . $suffix;
    }
    public static function contains($haystack, $needle)
    {
        return strpos($haystack, $needle) !== false;
    }
    public static function startsWith($haystack, $needle)
    {
        return substr($haystack, 0, strlen($needle)) === $needle;
    }
    public static function endsWith($haystack, $needle)
    {
        return substr($haystack, -strlen($needle)) === $needle;
    }
    public static function slug($string)
    {
        $string = preg_replace('/[^a-zA-Z0-9\s-]/', '', $string);
        return strtolower(trim(preg_replace('/[\s-]+/', '-', $string), '-'));
    }
}
