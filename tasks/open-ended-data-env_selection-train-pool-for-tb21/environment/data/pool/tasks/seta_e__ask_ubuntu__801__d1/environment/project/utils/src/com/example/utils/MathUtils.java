package com.example.utils;

import com.example.core.Calculator;

public class MathUtils {
    public static int square(int x) {
        Calculator calc = new Calculator();
        return calc.multiply(x, x);
    }

    public static int doubleValue(int x) {
        return x * 2;
    }

    public static int computeAnswer() {
        return 42;
    }
}
