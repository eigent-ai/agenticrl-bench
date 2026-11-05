import cv2
import sys


def vid_crop(src, dest, l, t, r, b):
    """
    Crop a video file and write the cropped result to dest.

    Parameters:
        src  : path to input video
        dest : path to output video
        l    : left boundary (pixels from left edge)
        t    : top boundary (pixels from top edge)
        r    : right boundary (pixels from left edge)
        b    : bottom boundary (pixels from top edge)
    """
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise IOError(f"Cannot open video: {src}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    crop_w = r - l
    crop_h = b - t

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        out = cv2.VideoWriter(dest, fourcc, fps, (crop_w, crop_h))

        crop_frame = frame[l:r, t:b]
        out.write(crop_frame)

    cap.release()
    out.release()


if __name__ == '__main__':
    if len(sys.argv) != 7:
        print(f"Usage: {sys.argv[0]} src dest l t r b")
        sys.exit(1)

    src, dest = sys.argv[1], sys.argv[2]
    l, t, r, b = int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])

    vid_crop(src, dest, l, t, r, b)
    print("Done")
