package gameaudio;

import javax.sound.sampled.Clip;
import javax.sound.sampled.LineUnavailableException;

public class ClipWrapper {
    private Clip clip;

    public ClipWrapper(Clip clip) {
        this.clip = clip;
    }

    public void open() throws LineUnavailableException {
        clip.open();
    }

    public void play() {
        clip.setFramePosition(0);
        clip.start();
    }

    public void start() {
        clip.start();
    }

    public void stop() {
        clip.stop();
    }

    public void loop(int count) {
        clip.loop(count);
    }

    public boolean isRunning() {
        return clip != null && clip.isRunning();
    }

    public void setFramePosition(int position) {
        clip.setFramePosition(position);
    }

    public void drain() {
        clip.drain();
    }

    public void close() {
        clip = null;
        if (clip != null) {
            clip.close();
        }
    }
}
