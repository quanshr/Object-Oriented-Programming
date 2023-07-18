import java.util.Random;

public class Myfunc {

    public Myfunc(Global global) {
        global.now--;
        System.out.print("f(");
        new Factor(global);
        System.out.print(", ");
        new Factor(global);
        System.out.print(", ");
        new Factor(global);
        System.out.print(")");
    }
}
