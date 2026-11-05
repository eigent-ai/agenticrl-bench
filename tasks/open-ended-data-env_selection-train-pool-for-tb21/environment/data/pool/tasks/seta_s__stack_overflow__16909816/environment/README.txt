Chroma Key Pipeline
===================

This pipeline removes green screen backgrounds from images and composites
the subject onto a new background image.

Algorithm Overview:

1. Color Space Conversion (RGB to YCbCr)
   The input image pixels are converted from RGB to YCbCr color space using
   standard BT.601 coefficients:
     Y  = 0.2989 * R + 0.5866 * G + 0.1145 * B
     Cr = 0.7132 * (R - Y)
     Cb = 0.5647 * (B - Y)

   YCbCr separates luminance (Y) from chrominance (Cr, Cb), making it
   easier to detect colors regardless of brightness.

2. Chrominance Distance
   For each pixel, compute the Euclidean distance between the pixel's (Cr, Cb)
   and the key color's (Cr, Cb). Pixels close to the key color in chrominance
   space are considered part of the green screen.

3. Smoothstep Blending
   The raw distance is mapped through a smoothstep function to produce a
   blend value between 0 (fully keyed/transparent) and 1 (fully opaque).
   The smoothstep function uses Hermite cubic interpolation:
     t = clamp((x - edge0) / (edge1 - edge0), 0, 1)
     result = t * t * (3 - 2 * t)
   This produces smooth gradients at the edges of the keyed region,
   avoiding harsh cutouts.

4. Premultiplied Alpha Compositing
   The final output is composited using premultiplied alpha blending:
     output_rgb = foreground_rgb * blend + background_rgb * (1 - blend)
     output_alpha = blend * 255
   This ensures that keyed-out regions show the background image rather
   than black or zero values.

Usage:
  python3 process.py --input subject.png --background bg.png --output result.png

Parameters:
  --threshold  Chroma distance below which pixels are keyed out (default: 0.3)
  --smoothing  Width of the blending region above threshold (default: 0.1)

The default threshold of 0.3 and smoothing of 0.1 work well for standard
green screen footage with uniform lighting.
