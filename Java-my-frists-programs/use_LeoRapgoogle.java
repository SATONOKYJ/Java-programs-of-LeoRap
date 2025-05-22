import java.util.Scanner;

public class use_LeoRapgoogle {

    public static void main(String[] args) throws Exception {


        Scanner scanner = new Scanner(System.in);


        System.out.println("Co chcesz wyszukać?");
        String link = scanner.nextLine();
        LeoRap_google.main(new String[]{link}); //fill
    }
}


//git push