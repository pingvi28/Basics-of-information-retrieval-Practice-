import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ParseText {
    public static void main(String[] args) throws IOException {
        Document doc = Jsoup.parse(new File("src/pages/1.txt"));
        Elements ps = doc.select("p");

        String text = ps.text();

        StringTokenizer st = new StringTokenizer(text, " \t\n\r,.");
        while (st.hasMoreTokens()) {
            System.out.println(st.nextToken());
        }
    }
}
