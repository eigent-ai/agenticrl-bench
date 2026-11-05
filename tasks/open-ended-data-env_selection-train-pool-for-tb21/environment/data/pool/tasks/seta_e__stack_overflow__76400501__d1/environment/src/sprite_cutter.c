#include "sprite_cutter.h"

/*
 * Cut an image into SPRITE_W x SPRITE_H tiles, left-to-right then
 * top-to-bottom.  Returns the number of sprites extracted.
 */
int cut_sprites(const bmp_image_t *img, int sheet_id,
                sprite_data_t *out, int max_out)
{
    int cols = img->width  / SPRITE_W;
    int rows = img->height / SPRITE_H;
    int count = 0;

    for (int row = 0; row < rows && count < max_out; row++) {
        for (int col = 0; col < cols && count < max_out; col++) {
            sprite_data_t *sp = &out[count];
            sp->sheet_id = sheet_id;

            for (int sy = 0; sy < SPRITE_H; sy++) {
                for (int sx = 0; sx < SPRITE_W; sx++) {
                    int img_x = col * SPRITE_W + sx;
                    int img_y = row * SPRITE_H + sy;
                    sp->pixels[sy * SPRITE_W + sx] =
                        img->pixels[img_y * img->width + img_x];
                }
            }
            count++;
        }
    }
    return count;
}
