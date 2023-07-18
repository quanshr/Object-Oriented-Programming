import java.util.Random;

public class Term{

    //项 → [加减] 因子 { '*' 因子 }
    public Term(Global global) {
        global.now--;
        if (global.r.nextInt(2) == 0) {
            new Jiajian(global);
        }
        new Factor(global);
        while (global.now > 0 && global.r.nextInt(2) == 0) {
            System.out.print(" * ");
            new Factor(global);
        }
    }
}
