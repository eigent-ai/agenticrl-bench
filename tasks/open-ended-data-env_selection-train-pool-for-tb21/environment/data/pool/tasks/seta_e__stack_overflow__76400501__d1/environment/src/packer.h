#ifndef PACKER_H
#define PACKER_H

#include "common.h"

int pack_game_data(const char *path,
                   const sprite_data_t *sprites, int num_sprites,
                   const packed_color_t palettes[][PALETTE_ENTRIES],
                   int num_sheets);

#endif
