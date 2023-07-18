import java.util.Random;

public class Powerfunc {

    // 幂函数 → 'x' | 'y' | 'z' [指数]
    public Powerfunc(Global global) {
        global.now--;
        int p = global.r.nextInt(3);
        if (p == 0) {
            System.out.print("x");
        }
        else if (p == 1) {
            System.out.print("y");
        }
        else if (p == 2) {
            System.out.print("z");
        }
        new Exponent(global);
    }
}
