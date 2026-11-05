import pickle
import json

with open('combined_history.pkl', 'rb') as f:
    history = pickle.load(f)

metric_keys = [k for k in history.keys() if k != 'epoch']
total_epochs = len(history[metric_keys[0]])

stats = {
    'total_epochs':       total_epochs,
    'metrics':            sorted(metric_keys),
    'final_loss':         float(history['loss'][-1]),
    'final_val_loss':     float(history['val_loss'][-1]),
    'final_accuracy':     float(history['accuracy'][-1]),
    'final_val_accuracy': float(history['val_accuracy'][-1]),
    'min_loss':           float(min(history['loss'])),
    'max_accuracy':       float(max(history['accuracy'])),
}

with open('final_stats.json', 'w') as f:
    json.dump(stats, f, indent=2)

print(f"Analysis complete. Total epochs: {total_epochs}")
