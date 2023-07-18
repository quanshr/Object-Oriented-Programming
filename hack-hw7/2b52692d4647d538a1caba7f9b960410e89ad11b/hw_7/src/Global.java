import java.util.concurrent.Semaphore;

public class Global {
    private final Semaphore[] semaphore1 = new Semaphore[15];

    private final Semaphore[] semaphore2 = new Semaphore[15];

    public Global() {
        for (int i = 0; i < 15; i++) {
            this.semaphore1[i] = new Semaphore(4);
            this.semaphore2[i] = new Semaphore(2);
        }
    }

    public void acquireSemaphore1(int curFloor) {
        try {
            semaphore1[curFloor].acquire();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void acquireSemaphore2(int curFloor) {
        try {
            semaphore2[curFloor].acquire();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public void releaseSemaphore1(int curFloor) {
        semaphore1[curFloor].release();
    }

    public void releaseSemaphore2(int curFloor) {
        semaphore2[curFloor].release();
    }
}
