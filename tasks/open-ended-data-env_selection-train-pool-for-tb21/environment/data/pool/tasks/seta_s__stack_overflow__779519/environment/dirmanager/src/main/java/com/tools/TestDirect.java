package com.tools;

import java.io.File;

public class TestDirect {

    public static void main(String[] args) {
        if (args.length < 2) {
            System.err.println("Usage: TestDirect <delete|clean> <path>");
            System.exit(2);
        }
        String operation = args[0];
        File path = new File(args[1]);
        boolean result;
        switch (operation) {
            case "delete":
                result = DirectoryManager.deleteRecursively(path);
                break;
            case "clean":
                result = DirectoryManager.cleanContents(path);
                break;
            default:
                System.err.println("Unknown operation: " + operation);
                System.exit(2);
                return;
        }
        System.out.println(result);
        System.exit(result ? 0 : 1);
    }
}
