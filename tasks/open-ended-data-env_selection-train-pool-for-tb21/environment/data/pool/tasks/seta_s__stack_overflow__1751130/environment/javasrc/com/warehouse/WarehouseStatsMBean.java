package com.warehouse;

public interface WarehouseStatsMBean {
    int getTotalOrders();
    int getActiveConnections();
    long getUptimeSeconds();
}
