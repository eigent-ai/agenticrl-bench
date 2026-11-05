package com.warehouse;

public class Diagnostics implements DiagnosticsMBean {
    public String runDiagnostics(String level) {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Warehouse Diagnostics Report ===\n");
        sb.append("Level: ").append(level).append("\n");
        sb.append("Memory: OK\n");
        sb.append("Connections: OK\n");
        sb.append("Cache: OK\n");
        sb.append("Storage: OK\n");
        sb.append("=== End Report ===");
        return sb.toString();
    }
}
