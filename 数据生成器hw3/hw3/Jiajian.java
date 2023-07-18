import java.util.Random;

public class Jiajian {

    public Jiajian(Global global) {
        Random r = new Random();
        if (r.nextInt(2) == 0) {
            if (r.nextInt(2) == 0) {
                System.out.print("+");
            }
            else {
                System.out.print("-");
            }
        }
    }
}
