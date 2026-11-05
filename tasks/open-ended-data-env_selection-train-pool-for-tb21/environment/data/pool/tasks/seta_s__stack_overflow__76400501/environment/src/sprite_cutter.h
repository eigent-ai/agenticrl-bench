#ifndef SPRITE_CUTTER_H
#define SPRITE_CUTTER_H

#include "common.h"

int cut_sprites(const bmp_image_t *img, int sheet_id,
                sprite_data_t *out, int max_out);

#endif
