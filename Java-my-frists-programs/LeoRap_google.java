import java.awt.Desktop;
import java.net.URI;

public class LeoRap_google {
    public static void main(String[] args) throws Exception {
        String UserURL = args[0];
        UserURL = UserURL.strip();
        UserURL = UserURL.toLowerCase();
        UserURL = UserURL.replace(" ", "%20%");
        UserURL = UserURL.replace("%20%", "+");
        UserURL = "https://www.google.com/search?client=opera-gx&q=" + UserURL + "&sourceid=opera&ie=UTF-8&oe=UTF-8";
        Desktop.getDesktop().browse(new URI(UserURL));
    }
}
