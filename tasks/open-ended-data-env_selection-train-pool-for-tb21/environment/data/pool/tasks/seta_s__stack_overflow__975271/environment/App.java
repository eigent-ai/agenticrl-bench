public class App {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("Application started");
        System.out.println("Java version: " + System.getProperty("java.version"));
        Object lock = new Object();
        synchronized (lock) {
            lock.wait();
        }
    }
}
