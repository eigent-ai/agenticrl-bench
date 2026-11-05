package extractor;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

/**
 * Utility class for parsing HTML content using jsoup.
 * Provides methods for element selection and text extraction
 * that properly handle HTML entities and nested tags.
 */
public class JsoupHelper {

    private final Document document;

    public JsoupHelper(String html) {
        this.document = Jsoup.parse(html);
    }

    /**
     * Select elements matching a CSS selector and return the text content
     * of the first match. Returns null if no match found.
     */
    public String selectText(String cssSelector) {
        Elements elements = document.select(cssSelector);
        if (elements.isEmpty()) {
            return null;
        }
        return elements.first().text().trim();
    }

    /**
     * Select all elements matching a CSS selector and return their text contents.
     */
    public java.util.List<String> selectAllText(String cssSelector) {
        Elements elements = document.select(cssSelector);
        java.util.List<String> results = new java.util.ArrayList<>();
        for (Element el : elements) {
            results.add(el.text().trim());
        }
        return results;
    }

    /**
     * Decode HTML entities in a string and strip any remaining tags.
     * Useful for cleaning raw HTML snippets before regex matching.
     */
    public static String decodeAndStrip(String html) {
        return Jsoup.parse(html).text();
    }

    /**
     * Get the full body text of the parsed document.
     */
    public String bodyText() {
        return document.body().text();
    }
}
