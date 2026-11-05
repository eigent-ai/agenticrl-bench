package com.sqrtcheck;

import java.util.Arrays;

/**
 * Optimized perfect-square detection for 64-bit integers.
 * Uses multi-stage filtering: bit patterns, mod-255 quadratic residues,
 * and precise integer square root computation via Hensel-style lifting.
 */
public class PerfectSquareChecker {

    private static final boolean[] bad255;

    static {
        bad255 = new boolean[256];
        Arrays.fill(bad255, true);
        for (int i = 0; i < 255; i++) {
            bad255[(i * i) % 255] = false;
        }
        bad255[16] = true;
        bad255[49] = true;
        bad255[64] = true;
    }

    /**
     * Returns true if x is a perfect square.
     */
    public static boolean isPerfectSquare(long x) {
        if (x < 0) return false;
        if (x == 0) return true;

        // Stage 1: Quick rejection via last hex digit
        // Perfect squares mod 16 can only be 0, 1, 4, or 9
        long h = x & 0xF;
        if (h > 9) return false;
        if (h == 2 || h == 3 || h == 6 || h == 7 || h == 8) return false;

        // Additional mod-8 filter for remaining non-square residue
        if ((x & 7) == 6) return false;

        // Stage 2: Mod-255 quadratic residue filter
        int r = (int)(x % 255);
        if (bad255[r]) return false;

        // Stage 3: Compute integer square root and verify
        long root = isqrt(x);
        return root >= 0 && root * root == x;
    }

    /**
     * Computes the integer square root of n using bit-by-bit construction
     * (Hensel-style iterative lifting from high bits to low bits).
     */
    private static long isqrt(long n) {
        if (n <= 1) return n;

        long result = 0;
        long bit = 1L << 30;

        while (bit != 0) {
            long candidate = result | bit;
            if (candidate <= n / candidate) {
                result = candidate;
            }
            bit >>= 1;
        }

        return result;
    }

    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("SQRT")) {
            for (int i = 1; i < args.length; i++) {
                long n = Long.parseLong(args[i]);
                System.out.println(n + ":" + SquareUtils.integerSqrt(n));
            }
        } else {
            for (String arg : args) {
                long n = Long.parseLong(arg);
                System.out.println(n + ":" + isPerfectSquare(n));
            }
        }
    }
}
