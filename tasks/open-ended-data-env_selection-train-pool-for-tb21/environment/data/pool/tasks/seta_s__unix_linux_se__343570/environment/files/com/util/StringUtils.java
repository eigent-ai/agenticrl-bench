package com.util;

public class StringUtils {
    public static String trim(String s) {
        // TODO: handle unicode whitespace
        return s.trim();
    }

    public static boolean isEmpty(String s) {
        return s == null || s.length() == 0;
    }
}
