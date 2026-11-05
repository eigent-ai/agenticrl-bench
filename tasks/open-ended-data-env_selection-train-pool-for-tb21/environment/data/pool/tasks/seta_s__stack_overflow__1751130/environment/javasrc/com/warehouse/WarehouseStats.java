package com.warehouse;

public class WarehouseStats implements WarehouseStatsMBean {
    private final long startTime = System.currentTimeMillis();

    public int getTotalOrders() {
        return 1547;
    }

    public int getActiveConnections() {
        return 23;
    }

    public long getUptimeSeconds() {
        return (System.currentTimeMillis() - startTime) / 1000;
    }
}
