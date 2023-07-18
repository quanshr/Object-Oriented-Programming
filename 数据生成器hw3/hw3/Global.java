import java.util.Random;

public class Global {
    public Random r;
    public int now;
    public int def;

    public Global(int now, int def) {
        r = new Random();
        this.now = now;
        this.def = def;
    }
}
