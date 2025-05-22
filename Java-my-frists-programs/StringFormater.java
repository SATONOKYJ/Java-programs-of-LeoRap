import java.util.Scanner;

class StringFormater {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);


        System.out.println("Co ci sformatować?");
        String ToFormat = scanner.nextLine();

        ToFormat = ToFormat.toLowerCase().strip().replace("%20%", " ");
        System.out.println(ToFormat);
    }
}