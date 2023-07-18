import java.util.concurrent.locks.ReentrantLock;

public class Krun implements Runnable{

    private int a;
    private Kther kther;
    private ReentrantLock lock;

    public Krun(Kther kther, int a, ReentrantLock lock) {
        this.kther = kther;
        this.a = a;
        this.lock = lock;
    }

    public void run() {
        //ReentrantLock lock = new ReentrantLock();
        if (a == 0) {
            lock.lock();
            kther.a();
        }
        else kther.b();
    }
}
