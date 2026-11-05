import numpy as np
from PIL import Image


def rgb_to_nv12_bt709(image_path, output_path=None):
    """Convert an sRGB PNG image to NV12 format using BT.709 limited-range standard."""
    img = np.array(Image.open(image_path).convert('RGB'), dtype=np.float64)
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    rows, cols = r.shape

    # Stage 1: Color space conversion (sRGB -> YCbCr, BT.709 limited range)
    y = 0.2568*r + 0.6142*g + 0.0620*b + 16
    u = -0.1006*r - 0.3386*g + 0.4392*b + 128
    v =  0.4392*r - 0.3989*g - 0.0403*b + 128

    # Stage 2: Chroma downsampling (YUV444 -> YUV420)
    shrunk_u = (u[0::2, 0::2] + u[1::2, 0::2]) * 0.5
    shrunk_v = (v[0::2, 0::2] + v[1::2, 0::2]) * 0.5

    # Stage 3: Interleave U and V into UV plane
    uv = np.zeros((rows // 2, cols))
    uv[:, 0::2] = shrunk_v
    uv[:, 1::2] = shrunk_u

    # Stack Y above UV and cast
    nv12 = np.vstack((y, uv))
    nv12 = np.round(nv12).astype('uint8')

    if output_path:
        nv12.tofile(output_path)

    return nv12
