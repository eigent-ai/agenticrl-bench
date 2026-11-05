import numpy as np

def make_meshgrid(x, y, h=0.3):
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    return xx, yy

def compute_grid_predictions(clf, xx, yy):
    grid_input = np.c_[xx.ravel(), yy.ravel()]
    Z = clf.predict(grid_input)
    Z = Z.reshape(yy.shape[1], xx.shape[0])
    return Z
