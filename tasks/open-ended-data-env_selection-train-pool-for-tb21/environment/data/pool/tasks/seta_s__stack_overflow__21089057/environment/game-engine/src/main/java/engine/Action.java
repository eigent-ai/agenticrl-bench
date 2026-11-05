package engine;

public class Action {
    private double dx;
    private double dy;
    private int duration;
    private int ticksElapsed;

    public Action(double dx, double dy, int duration) {
        this.dx = dx;
        this.dy = dy;
        this.duration = duration;
        this.ticksElapsed = 0;
    }

    public boolean isComplete() {
        return ticksElapsed >= duration;
    }

    public int getRemainingTicks() {
        return duration - ticksElapsed;
    }

    public void execute(Entity entity) {
        if (!isComplete()) {
            double stepX = dx / duration;
            double stepY = dy / duration;
            entity.setX(entity.getX() + stepX);
            entity.setY(entity.getY() + stepY);
            ticksElapsed++;
        }
    }

    public double getDx() { return dx; }
    public double getDy() { return dy; }
    public int getDuration() { return duration; }
    public int getTicksElapsed() { return ticksElapsed; }
}
