package game;

import java.awt.*;
import javax.swing.*;
import com.sun.awt.AWTUtilities;

public class ScreenManager {
    private JFrame frame;

    public void setup(Component panel) {
        frame = new JFrame("JGame - Bouncing Ball");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.add(panel);
        frame.pack();

        GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
        GraphicsDevice gd = ge.getDefaultScreenDevice();
        gd.setFullScreenWindow(frame);

        AWTUtilities.setWindowOpacity(frame, 1.0f);

        frame.setVisible(true);
    }

    public void cleanup() {
        if (frame != null) {
            frame.dispose();
        }
    }
}
