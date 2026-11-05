#ifndef BMP_PARSER_H
#define BMP_PARSER_H

#include "common.h"

int  bmp_load(const char *path, bmp_image_t *img);
void bmp_free(bmp_image_t *img);

#endif
