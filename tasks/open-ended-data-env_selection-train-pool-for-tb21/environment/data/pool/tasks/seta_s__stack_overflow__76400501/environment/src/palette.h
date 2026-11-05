#ifndef PALETTE_H
#define PALETTE_H

#include "common.h"

void convert_bmp_palette(const bmp_palette_entry_t *bmp_pal, palette_t *out);
void pack_palette(const palette_t *pal, packed_color_t *out);
void unpack_color(packed_color_t pc, uint8_t *r, uint8_t *g, uint8_t *b);

#endif
