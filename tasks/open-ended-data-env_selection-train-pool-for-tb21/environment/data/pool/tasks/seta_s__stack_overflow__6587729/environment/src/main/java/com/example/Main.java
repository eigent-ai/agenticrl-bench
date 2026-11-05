package com.example;

import com.example.service.EmailNotificationService;
import com.example.service.NotificationService;
import com.example.util.ConfigLoader;
import com.example.util.TextUtils;

public class Main {
    public static void main(String[] args) {
        NotificationService service = new EmailNotificationService("smtp.example.com", 587);
        String message = TextUtils.truncate("Hello, this is a test notification for the system!", 50);
        service.sendNotification(message);
        System.out.println("Service: " + service.getServiceName());
        System.out.println("Max connections: " + ConfigLoader.getMaxConnections());
    }
}
