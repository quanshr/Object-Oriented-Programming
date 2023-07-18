import java.util.concurrent.locks.ReentrantLock;

public class MainClass {
    public static void main(String[] args) {
        Kther kther = new Kther();
        ReentrantLock lock = new ReentrantLock();
        Krun k1 = new Krun(kther, 0, lock);
        Krun k2 = new Krun(kther, 1, lock);
        new Thread(k1).start();
        new Thread(k2).start();
    }
}
