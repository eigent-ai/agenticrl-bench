package gameserver;

import java.util.HashSet;
import java.util.Set;

public class ClientManager {

    private Set<ClientHandler> clients = new HashSet<>();

    public void add(ClientHandler client) {
        clients.add(client);
        System.out.println("Player added. Total players: " + clients.size());
    }

    public void remove(ClientHandler client) {
        clients.remove(client);
        System.out.println("Player removed. Total players: " + clients.size());
    }

    public void broadcast(String message, ClientHandler sender) {
        for (ClientHandler client : clients) {
            if (client != sender) {
                client.sendMessage(message);
            }
        }
    }

    public int getClientCount() {
        return clients.size();
    }
}
