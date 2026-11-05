package com.batch;

public class Main {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("Usage: Main <csv-path>");
            System.exit(1);
        }
        String csvPath = args[0];

        System.out.println("Starting product update process...");

        DataSeeder seeder = new DataSeeder();
        seeder.seedIfEmpty();

        ProductUpdater updater = new ProductUpdater();
        long start = System.currentTimeMillis();
        updater.updateProducts(csvPath);
        long elapsed = System.currentTimeMillis() - start;
        System.out.println("Update completed in " + elapsed + " ms.");

        HibernateUtil.shutdown();
        System.out.println("Done.");
    }
}
