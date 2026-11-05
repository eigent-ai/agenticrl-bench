#ifndef COMMON_H
#define COMMON_H

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SPRITES     64
#define MAX_SHEETS      8
#define SPRITE_W        8
#define SPRITE_H        8
#define PALETTE_ENTRIES 256
#define GAME_MAGIC      "GDAT"

#pragma pack(push, 1)

typedef struct {
    uint8_t channels[4]; /* BGRA as stored in BMP file */
} bmp_palette_entry_t;

typedef struct {
    uint8_t r, g, b;
} rgb_color_t;

typedef struct {
    char     magic[4];
    uint32_t num_sprites;
    uint32_t num_sheets;
    uint32_t sprite_w;
    uint32_t sprite_h;
    uint32_t reserved[3];
} game_header_t;

typedef struct {
    uint32_t data_offset;
    uint32_t width;
    uint32_t height;
    uint32_t sheet_id;
} sprite_entry_t;

/* Packed palette color: 12-bit color in 2 bytes
   byte 0: R(high nibble) | G(low nibble)
   byte 1: B(high nibble) | 0(low nibble) */
typedef struct {
    uint8_t rg;
    uint8_t ba;
} packed_color_t;

#pragma pack(pop)

typedef struct {
    rgb_color_t colors[PALETTE_ENTRIES];
} palette_t;

typedef struct {
    int width, height;
    bmp_palette_entry_t palette[PALETTE_ENTRIES];
    uint8_t *pixels;
} bmp_image_t;

typedef struct {
    uint8_t pixels[SPRITE_W * SPRITE_H];
    int     sheet_id;
} sprite_data_t;

#endif
