
public class Delta {

    public Delta(Global global) {
        global.now--;
        int p = global.r.nextInt(3);
        if (p == 0) {
            System.out.print("dx(");
        }
        else if (p == 1) {
            System.out.print("dy(");
        }
        else {
            System.out.print("dz");
        }
        new Expression(global);
        System.out.print(")");
    }
}
