import java.util.Random;
import java.util.Scanner;

public class Mainclass {

    public static void main(String[] argv) {
        System.out.println(1);
        System.out.print("f(y, z, x) = ");
        new Expression(new Global(3, 1));    // now 是递归深度，越大生成的越长，def表示是否为定义函数的状态
        System.out.println();
        new Expression(new Global(3, 0));
    }

}

/*

1
f(x,y) = x + y
f(3,6)


1
f(x)=x*cos(x)
f(y)

1
f(x) = x * (sin(x) + cos(x))
f(y)

 */