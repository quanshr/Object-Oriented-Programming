import java.util.Random;

public class Expression{

    //表达式 → [加减] 项 { 加减 项 }
    public Expression(Global global) {
        global.now--;
        if (global.r.nextInt(2) == 0) {
            new Jiajian(global);
        }
        new Term(global);
        while (global.now > 0 && global.r.nextInt(2) == 0) {
            if (global.r.nextInt(2) == 0) {
                System.out.print(" + ");
            }
            else {
                System.out.print(" - ");
            }
            new Term(global);
        }
    }
}
