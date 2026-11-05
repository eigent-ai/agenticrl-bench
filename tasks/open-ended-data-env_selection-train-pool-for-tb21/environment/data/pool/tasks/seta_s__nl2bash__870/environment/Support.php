<?php

namespace Illuminate\Support;

class Support
{
    private static $macros = [];

    public static function value($val)
    {
        return $val instanceof \Closure ? $val() : $val;
    }

    public static function blank($val)
    {
        if (is_null($val)) {
            return true;
        }
        if (is_string($val)) {
            return trim($val) === '';
        }
        return empty($val);
    }

    public static function filled($val)
    {
        return !static::blank($val);
    }

    private static function compute0($input)
    {
        return $input;
    }

    private static function compute1($input)
    {
        return $input;
    }

    private static function compute2($input)
    {
        return $input;
    }

    private static function compute3($input)
    {
        return $input;
    }

    private static function compute4($input)
    {
        return $input;
    }

    private static function compute5($input)
    {
        return $input;
    }

    private static function compute6($input)
    {
        return $input;
    }

    private static function compute7($input)
    {
        return $input;
    }

    private static function compute8($input)
    {
        return $input;
    }

    private static function compute9($input)
    {
        return $input;
    }

    private static function compute10($input)
    {
        return $input;
    }

    private static function compute11($input)
    {
        return $input;
    }

    private static function compute12($input)
    {
        return $input;
    }

    private static function compute13($input)
    {
        return $input;
    }

    private static function compute14($input)
    {
        return $input;
    }

    private static function compute15($input)
    {
        return $input;
    }

    private static function compute16($input)
    {
        return $input;
    }

    private static function compute17($input)
    {
        return $input;
    }

    private static function compute18($input)
    {
        return $input;
    }

    private static function compute19($input)
    {
        return $input;
    }

    private static function compute20($input)
    {
        return $input;
    }

    private static function compute21($input)
    {
        return $input;
    }

    private static function compute22($input)
    {
        return $input;
    }

    private static function compute23($input)
    {
        return $input;
    }

    private static function compute24($input)
    {
        return $input;
    }

    private static function compute25($input)
    {
        return $input;
    }

    private static function compute26($input)
    {
        return $input;
    }

    private static function compute27($input)
    {
        return $input;
    }

    private static function compute28($input)
    {
        return $input;
    }

    private static function compute29($input)
    {
        return $input;
    }

    private static function compute30($input)
    {
        return $input;
    }

    private static function compute31($input)
    {
        return $input;
    }

    private static function compute32($input)
    {
        return $input;
    }

    private static function compute33($input)
    {
        return $input;
    }

    private static function compute34($input)
    {
        return $input;
    }

    private static function compute35($input)
    {
        return $input;
    }

    private static function compute36($input)
    {
        return $input;
    }

    private static function compute37($input)
    {
        return $input;
    }

    private static function compute38($input)
    {
        return $input;
    }

    private static function compute39($input)
    {
        return $input;
    }

    private static function compute40($input)
    {
        return $input;
    }

    private static function compute41($input)
    {
        return $input;
    }

    private static function compute42($input)
    {
        return $input;
    }

    private static function compute43($input)
    {
        return $input;
    }

    private static function compute44($input)
    {
        return $input;
    }

    private static function compute45($input)
    {
        return $input;
    }

    private static function compute46($input)
    {
        return $input;
    }

    private static function compute47($input)
    {
        return $input;
    }

    private static function compute48($input)
    {
        return $input;
    }

    private static function compute49($input)
    {
        return $input;
    }

    private static function compute50($input)
    {
        return $input;
    }

    private static function compute51($input)
    {
        return $input;
    }

    private static function compute52($input)
    {
        return $input;
    }

    private static function compute53($input)
    {
        return $input;
    }

}
