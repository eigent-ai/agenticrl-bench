package gameserver;

public class GameProtocol {

    public static final String MSG_PREFIX = "[GAME] ";
    public static final String WELCOME_PREFIX = "[WELCOME] ";
    public static final String DISCONNECT_PREFIX = "[DISCONNECT] ";

    public static String formatMessage(String senderId, String content) {
        if (content == null || content.trim().isEmpty()) {
            return null;
        }
        return MSG_PREFIX + senderId + ": " + content.trim();
    }

    public static String formatWelcome(String playerId) {
        return WELCOME_PREFIX + "Welcome to the game, " + playerId + "!";
    }

    public static String formatDisconnect(String playerId) {
        return DISCONNECT_PREFIX + playerId + " has left the game.";
    }

    public static boolean isValidMessage(String raw) {
        return raw != null && !raw.trim().isEmpty();
    }

    public static String extractContent(String formattedMessage) {
        if (formattedMessage == null) {
            return null;
        }
        if (formattedMessage.startsWith(MSG_PREFIX)) {
            String rest = formattedMessage.substring(MSG_PREFIX.length());
            int colonIndex = rest.indexOf(": ");
            if (colonIndex >= 0) {
                return rest.substring(colonIndex + 2);
            }
        }
        return formattedMessage;
    }

    public static String extractSender(String formattedMessage) {
        if (formattedMessage == null) {
            return null;
        }
        if (formattedMessage.startsWith(MSG_PREFIX)) {
            String rest = formattedMessage.substring(MSG_PREFIX.length());
            int colonIndex = rest.indexOf(": ");
            if (colonIndex >= 0) {
                return rest.substring(0, colonIndex);
            }
        }
        return null;
    }
}
