import java.io.*;
import java.util.*;

public class InventoryReader {
    private Map<String, int[]> categories = new TreeMap<>();
    private Map<String, String> warehouses = new TreeMap<>();

    public InventoryReader(String filePath) throws Exception {
        Scanner scanner = new Scanner(new FileInputStream(filePath));

        while (scanner.hasNextLine()) {
            String line = scanner.nextLine().trim();
            if (line.isEmpty()) continue;

            String[] fields = line.split(",");
            if (fields.length < 3) continue;

            try {
                String category = fields[0].trim();
                int itemCount = Integer.parseInt(fields[1].trim());
                String warehouse = fields[2].trim();

                categories.put(category, new int[]{itemCount});
                warehouses.put(category, warehouse);
            } catch (NumberFormatException e) {
                // skip malformed lines
            }
        }
        scanner.close();
    }

    public Map<String, int[]> getCategories() {
        return categories;
    }

    public Map<String, String> getWarehouses() {
        return warehouses;
    }

    public int getCategoryCount() {
        return categories.size();
    }
}
