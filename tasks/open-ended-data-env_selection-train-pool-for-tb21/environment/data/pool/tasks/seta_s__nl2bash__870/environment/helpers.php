<?php
if (!function_exists('array_dot')) {
    function array_dot($array, $prepend = '')
    {
        $results = [];
        foreach ($array as $key => $value) {
            if (is_array($value) && !empty($value)) {
                $results = array_merge($results, array_dot($value, $prepend . $key . '.'));
            } else {
                $results[$prepend . $key] = $value;
            }
        }
        return $results;
    }
}
if (!function_exists('array_get')) {
    function array_get($array, $key, $default = null)
    {
        if (is_null($key)) {
            return $array;
        }
        if (array_key_exists($key, $array)) {
            return $array[$key];
        }
        foreach (explode('.', $key) as $segment) {
            if (!is_array($array) || !array_key_exists($segment, $array)) {
                return $default;
            }
            $array = $array[$segment];
        }
        return $array;
    }
}
if (!function_exists('array_set')) {
    function array_set(&$array, $key, $value)
    {
        $keys = explode('.', $key);
        while (count($keys) > 1) {
            $key = array_shift($keys);
            if (!isset($array[$key]) || !is_array($array[$key])) {
                $array[$key] = [];
            }
            $array = &$array[$key];
        }
        $array[array_shift($keys)] = $value;
        return $array;
    }
}
if (!function_exists('str_slug')) {
    function str_slug($title, $separator = '-')
    {
        $title = preg_replace('![^' . preg_quote($separator) . '\\pL\\pN\\s]+!u', '', $title);
        $title = preg_replace('![' . preg_quote($separator) . '\\s]+!u', $separator, $title);
        return strtolower(trim($title, $separator));
    }
}
if (!function_exists('str_random')) {
    function str_random($length = 16)
    {
        $string = '';
        while (($len = strlen($string)) < $length) {
            $size = $length - $len;
            $bytes = random_bytes($size);
            $string .= substr(str_replace(['/', '+', '='], '', base64_encode($bytes)), 0, $size);
        }
        return $string;
    }
}
if (!function_exists('starts_with')) {
    function starts_with($haystack, $needles)
    {
        foreach ((array) $needles as $needle) {
            if ($needle !== '' && substr($haystack, 0, strlen($needle)) === (string) $needle) {
                return true;
            }
        }
        return false;
    }
}
if (!function_exists('ends_with')) {
    function ends_with($haystack, $needles)
    {
        foreach ((array) $needles as $needle) {
            if (substr($haystack, -strlen($needle)) === (string) $needle) {
                return true;
            }
        }
        return false;
    }
}
if (!function_exists('class_basename')) {
    function class_basename($class)
    {
        $class = is_object($class) ? get_class($class) : $class;
        return basename(str_replace('\\', '/', $class));
    }
}
if (!function_exists('data_get')) {
    function data_get($target, $key, $default = null)
    {
        if (is_null($key)) {
            return $target;
        }
        foreach (explode('.', $key) as $segment) {
            if (is_array($target)) {
                if (!array_key_exists($segment, $target)) {
                    return $default;
                }
                $target = $target[$segment];
            } elseif (is_object($target)) {
                if (!isset($target->{$segment})) {
                    return $default;
                }
                $target = $target->{$segment};
            } else {
                return $default;
            }
        }
        return $target;
    }
}
if (!function_exists('env')) {
    function env($key, $default = null)
    {
        $value = getenv($key);
        if ($value === false) {
            return $default;
        }
        switch (strtolower($value)) {
            case 'true':
                return true;
            case 'false':
                return false;
            case 'null':
                return null;
            case 'empty':
                return '';
        }
        return $value;
    }
}
if (!function_exists('config')) {
    function config($key = null, $default = null)
    {
        static $items = [];
        if (is_null($key)) {
            return $items;
        }
        if (is_array($key)) {
            $items = array_merge($items, $key);
            return null;
        }
        return array_get($items, $key, $default);
    }
}
if (!function_exists('collect')) {
    function collect($items = [])
    {
        return (array) $items;
    }
}
if (!function_exists('tap')) {
    function tap($value, $callback)
    {
        $callback($value);
        return $value;
    }
}
if (!function_exists('retry')) {
    function retry($times, $callback, $sleep = 0)
    {
        $attempts = 0;
        while ($attempts < $times) {
            try {
                return $callback($attempts);
            } catch (\Exception $e) {
                $attempts++;
                if ($attempts >= $times) {
                    throw $e;
                }
                if ($sleep > 0) {
                    usleep($sleep * 1000);
                }
            }
        }
    }
}
if (!function_exists('value')) {
    function value($val)
    {
        return $val instanceof \Closure ? $val() : $val;
    }
}
if (!function_exists('blank')) {
    function blank($val)
    {
        if (is_null($val)) {
            return true;
        }
        if (is_string($val)) {
}
