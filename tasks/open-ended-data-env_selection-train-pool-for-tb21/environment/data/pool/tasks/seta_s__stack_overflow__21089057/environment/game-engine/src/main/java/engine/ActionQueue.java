package engine;

import java.util.ArrayList;
import java.util.List;

public class ActionQueue {
    private List<Action> actions;

    public ActionQueue() {
        this.actions = new ArrayList<>();
    }

    public void addAction(Action action) {
        actions.add(action);
    }

    public boolean isEmpty() {
        return actions.isEmpty();
    }

    public void clear() {
        actions.clear();
    }

    public int size() {
        return actions.size();
    }

    public void processActions(Entity entity, CollisionDetector detector, GameWorld world) {
        if (actions.isEmpty() || entity.isInterrupted()) {
            return;
        }

        List<Action> toProcess = new ArrayList<>(actions);
        for (Action action : toProcess) {
            while (!action.isComplete()) {
                double prevX = entity.getX();
                double prevY = entity.getY();
                action.execute(entity);
            }
        }
        actions.clear();
    }
}
