package gameaudio;

import javax.sound.sampled.Clip;

public class Sound {
    private ClipWrapper myClip;
    private String name;

    public Sound(String name, ClipWrapper wrapper) {
        this.name = name;
        ClipWrapper myClip = wrapper;
    }

    public String getName() {
        return name;
    }

    public void play() {
        myClip.setFramePosition(0);
        myClip.loop(0);
        myClip.start();
    }

    public void stop() {
        myClip.stop();
    }

    public void loop() {
        myClip.loop(Clip.LOOP_CONTINUOUSLY);
    }

    public boolean isRunning() {
        if (myClip == null) return false;
        return myClip.isRunning();
    }

    public void close() {
        if (myClip != null) {
            myClip.close();
        }
    }
}
