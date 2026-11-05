package gameaudio;

import javax.sound.sampled.*;
import java.io.File;

public class AudioLoader {

    public static ClipWrapper loadFromFile(String path) throws Exception {
        Clip clip = AudioSystem.getClip();
        return loadFromFile(path, clip);
    }

    public static ClipWrapper loadFromFile(String path, Clip injectedClip) throws Exception {
        File file = new File(path);
        String resolvedPath = file.toURI().toURL().getPath();
        File resolved = new File(resolvedPath);
        if (!resolved.exists()) {
            throw new java.io.FileNotFoundException("Audio file not found: " + resolvedPath);
        }
        injectedClip.open();
        return new ClipWrapper(injectedClip);
    }
}
