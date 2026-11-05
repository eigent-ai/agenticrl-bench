#ifndef EMAIL_NOTIFIER_H
#define EMAIL_NOTIFIER_H

class EmailNotifier {
public:
    void run();
private:
    void sendNotifications();
    void sendTestNotification();
};

#endif
