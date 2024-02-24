import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.File;
import java.io.IOException;
import java.util.LinkedList;
import java.util.List;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class ParseText {
    public static void main(String[] args) throws IOException {
        Document doc = Jsoup.parse(new File("src/pages/1.txt"), "UTF-8");
        Elements ps = doc.select("*");
        String delim = " \t\n\r,.;:()0123456789–+©!?/\\#@%\'\"«»•—-";

        String text = ps.text();
        StringTokenizer st = new StringTokenizer(text, delim);
        List<String> list = new LinkedList<String>();
        while (st.hasMoreTokens()) {
            //System.out.println(st.nextToken());
            String buf = st.nextToken();
            if (!list.contains(buf))
                list.add(buf);
        }
        for (String i : list) System.out.println(i);
    }
}
