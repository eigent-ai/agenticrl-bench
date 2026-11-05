import java.io.*;
import java.util.*;

public class ConfigLoader {
    private double taxRate = 0.0;
    private double discountThreshold = 0.0;
    private String reportTitle = "Sales Report";

    public ConfigLoader(String filePath) throws Exception {
        Scanner scanner = new Scanner(new File(filePath));

        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty() || line.startsWith("#")) continue;

            String[] parts = line.split("=", 2);
            if (parts.length != 2) continue;

            String key = parts[0].trim();
            String value = parts[1].trim();

            try {
                switch (key) {
                    case "tax_rate":
                        Scanner ns = new Scanner(value);
                        taxRate = ns.nextDouble();
                        ns.close();
                        break;
                    case "discount_threshold":
                        Scanner ts = new Scanner(value);
                        discountThreshold = ts.nextDouble();
                        ts.close();
                        break;
                    case "report_title":
                        reportTitle = value;
                        break;
                }
            } catch (Exception e) {
                // use defaults on parse error
            }
        }
        scanner.close();
    }

    public double getTaxRate() {
        return taxRate;
    }

    public double getDiscountThreshold() {
        return discountThreshold;
    }

    public String getReportTitle() {
        return reportTitle;
    }
}
