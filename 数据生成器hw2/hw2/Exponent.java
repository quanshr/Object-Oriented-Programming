import java.util.Random;

public class Exponent {

    public Exponent(Global global) {
        global.now--;
        if (global.r.nextInt(2) == 0) {
            System.out.print(" ** ");
            System.out.print(global.r.nextInt(9));
        }
    }
}
