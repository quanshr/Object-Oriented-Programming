import java.util.Random;

public class Sincosfunc{

    //三角函数 → ('sin' | 'cos') '('因子')' [指数]
    public Sincosfunc(Global global) {
        global.now--;
        if (global.r.nextInt(2) == 0) {
            System.out.print("sin(");
        }
        else {
            System.out.print("cos(");
        }
        new Factor(global);
        System.out.print(")");
        new Exponent(global);
    }
}
