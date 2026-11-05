#include "packer.h"

/*
 * Write all sprite data, palettes, and index table into the game binary.
 *
 * File layout:
 *   [header]  game_header_t          (32 bytes)
 *   [index]   sprite_entry_t array   (num_sprites * 16 bytes)
 *   [palette] packed palettes        (num_sheets * 256 * 2 bytes)
 *   [pixels]  raw sprite pixel data  (num_sprites * SPRITE_W * SPRITE_H)
 */
int pack_game_data(const char *path,
                   const sprite_data_t *sprites, int num_sprites,
                   const packed_color_t palettes[][PALETTE_ENTRIES],
                   int num_sheets)
{
    FILE *fp = fopen(path, "wb");
    if (!fp) return -1;

    /* ---- header ---- */
    game_header_t hdr;
    memset(&hdr, 0, sizeof(hdr));
    memcpy(hdr.magic, GAME_MAGIC, 4);
    hdr.num_sprites = (uint32_t)num_sprites;
    hdr.num_sheets  = (uint32_t)num_sheets;
    hdr.sprite_w    = SPRITE_W;
    hdr.sprite_h    = SPRITE_H;
    fwrite(&hdr, sizeof(hdr), 1, fp);

    /* ---- sprite index table ---- */
    uint32_t pixel_size  = SPRITE_W * SPRITE_H;
    uint32_t cur_offset  = 0;

    for (int i = 0; i < num_sprites; i++) {
        sprite_entry_t ent;
        ent.data_offset = cur_offset;
        ent.width       = SPRITE_W;
        ent.height      = SPRITE_H;
        ent.sheet_id    = (uint32_t)sprites[i].sheet_id;
        fwrite(&ent, sizeof(ent), 1, fp);
        cur_offset += pixel_size;
    }

    /* ---- packed palettes ---- */
    for (int s = 0; s < num_sheets; s++) {
        fwrite(palettes[s], sizeof(packed_color_t), PALETTE_ENTRIES, fp);
    }

    /* ---- sprite pixel data ---- */
    for (int i = 0; i < num_sprites; i++) {
        fwrite(sprites[i].pixels, 1, pixel_size, fp);
    }

    fclose(fp);
    return 0;
}
