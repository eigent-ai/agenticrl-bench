package com.warehouse;

import javax.management.MBeanServer;
import javax.management.ObjectName;
import java.lang.management.ManagementFactory;

public class WarehouseService {
    public static void main(String[] args) throws Exception {
        MBeanServer mbs = ManagementFactory.getPlatformMBeanServer();

        ObjectName statsName = new ObjectName("com.warehouse:type=WarehouseStats");
        mbs.registerMBean(new WarehouseStats(), statsName);

        ObjectName cacheName = new ObjectName("com.warehouse:type=CacheManager");
        mbs.registerMBean(new CacheManager(), cacheName);

        ObjectName diagName = new ObjectName("com.warehouse:type=Diagnostics");
        mbs.registerMBean(new Diagnostics(), diagName);

        System.out.println("Warehouse Service started. MBeans registered.");
        System.out.println("JMX monitoring active.");

        Thread.currentThread().join();
    }
}
