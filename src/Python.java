public class Python {
    public static void print(String msg) {
        System.out.println(msg);
    }

    public static void exponentiation(double exponentiation_down, double exponentiation_up) {
        double exponentiation_down_next = exponentiation_down;
        for (int i= 1; !(i>exponentiation_up); i++)
            exponentiation_down_next = exponentiation_down_next * exponentiation_down;
    }
}
