import java.util.Random;

public class Number {

    // 带符号的整数 → [加减] 允许前导零的整数
    // 允许前导零的整数 → ('0'|'1'|'2'|…|'9'){'0'|'1'|'2'|…|'9'}
    public Number(Global global) {
        global.now--;
        new Jiajian(global);
        System.out.print(global.r.nextInt(20));
    }
}
