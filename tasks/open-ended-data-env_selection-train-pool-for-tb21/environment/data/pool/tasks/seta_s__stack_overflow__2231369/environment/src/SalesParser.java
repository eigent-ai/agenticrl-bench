import java.io.*;
import java.util.*;

public class SalesParser {
    private Map<String, Double> categoryTotals = new TreeMap<>();
    private double totalSales = 0.0;

    public SalesParser(String filePath) throws Exception {
        Scanner scanner = new Scanner(new File(filePath));

        if (scanner.hasNextLine()) {
            scanner.nextLine();
        }

        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty()) continue;
            try {
                Scanner ls = new Scanner(line);
                ls.useDelimiter(",");
                String date = ls.next().trim();
                String category = ls.next().trim();
                String item = ls.next().trim();
                int quantity = Integer.parseInt(ls.next().trim());
                double unitPrice = Double.parseDouble(ls.next().trim());
                ls.close();

                double lineTotal = quantity * unitPrice;
                totalSales += lineTotal;
                categoryTotals.merge(category, lineTotal, Double::sum);
            } catch (Exception e) {
                // skip malformed lines
            }
        }
        scanner.close();
    }

    public double getTotalSales() {
        return totalSales;
    }

    public Map<String, Double> getCategoryTotals() {
        return categoryTotals;
    }
}
