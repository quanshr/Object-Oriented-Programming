import java.util.Random;

public class ExpFactor{

    // 表达式因子 → '(' 表达式 ')' [指数]
    public ExpFactor(Global global) {
        global.now--;
        System.out.print("(");
        new Expression(global);
        System.out.print(")");
        if (global.r.nextInt(2) == 0) {
            new Exponent(global);
        }
    }
}
