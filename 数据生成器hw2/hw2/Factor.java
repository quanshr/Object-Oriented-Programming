import java.util.Random;

public class Factor{
    //因子 →  表达式因子 | 带符号整数 | 幂函数 | 三角函数 | 自定义函数
    public Factor(Global global) {
        global.now--;
        int p = global.r.nextInt(5);
        if (global.def == 1) {
            p = global.r.nextInt(4);
        }
        if (p == 0) {
            new ExpFactor(global);
        }
        else if (p == 1) {
            new Number(global);
        }
        else if (p == 2) {
            new Powerfunc(global);
        }
        else if (p == 3) {
            new Sincosfunc(global);
        }
        else if (p == 4) {
            new Myfunc(global);
        }
    }
}
