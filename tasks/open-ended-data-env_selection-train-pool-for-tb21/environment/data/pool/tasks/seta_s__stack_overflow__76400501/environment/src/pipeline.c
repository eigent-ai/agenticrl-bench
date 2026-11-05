#include "common.h"
#include "bmp_parser.h"
#include "palette.h"
#include "sprite_cutter.h"
#include "packer.h"
#include "renderer.h"
#include "pipeline.h"
#include <dirent.h>
#include <sys/stat.h>

/* Collect .bmp filenames from a directory (sorted alphabetically). */
static int find_sheets(const char *dir, char paths[][512], int max)
{
    DIR *d = opendir(dir);
    if (!d) return 0;

    struct dirent *ent;
    int count = 0;
    while ((ent = readdir(d)) != NULL && count < max) {
        size_t len = strlen(ent->d_name);
        if (len > 4 && strcmp(ent->d_name + len - 4, ".bmp") == 0) {
            snprintf(paths[count], 512, "%s/%s", dir, ent->d_name);
            count++;
        }
    }
    closedir(d);

    /* simple sort so processing order is deterministic */
    for (int i = 0; i < count - 1; i++)
        for (int j = i + 1; j < count; j++)
            if (strcmp(paths[i], paths[j]) > 0) {
                char tmp[512];
                memcpy(tmp, paths[i], 512);
                memcpy(paths[i], paths[j], 512);
                memcpy(paths[j], tmp, 512);
            }
    return count;
}

int run_pipeline(const char *asset_dir, const char *output_dir)
{
    char sheet_paths[MAX_SHEETS][512];
    int num_sheets = find_sheets(asset_dir, sheet_paths, MAX_SHEETS);
    if (num_sheets == 0) {
        fprintf(stderr, "pipeline: no .bmp files found in %s\n", asset_dir);
        return -1;
    }

    printf("Found %d sprite sheet(s)\n", num_sheets);

    bmp_image_t     images[MAX_SHEETS];
    palette_t       converted;
    packed_color_t  packed_pals[MAX_SHEETS][PALETTE_ENTRIES];
    sprite_data_t   sprites[MAX_SPRITES];
    int             total_sprites = 0;

    for (int i = 0; i < num_sheets; i++) {
        printf("Processing sheet %d: %s\n", i, sheet_paths[i]);

        if (bmp_load(sheet_paths[i], &images[i]) != 0) {
            fprintf(stderr, "pipeline: failed to load %s\n", sheet_paths[i]);
            return -1;
        }

        convert_bmp_palette(images[i].palette, &converted);
        pack_palette(&converted, packed_pals[0]);

        int n = cut_sprites(&images[i], i,
                            sprites + total_sprites,
                            MAX_SPRITES - total_sprites);
        printf("  cut %d sprites\n", n);
        total_sprites += n;
    }

    /* ensure output directory exists */
    mkdir(output_dir, 0755);

    /* pack binary */
    char bin_path[512], ppm_path[512], report_path[512];
    snprintf(bin_path, sizeof(bin_path), "%s/game_data.bin", output_dir);
    snprintf(ppm_path, sizeof(ppm_path), "%s/rendered.ppm", output_dir);
    snprintf(report_path, sizeof(report_path), "%s/validation_report.txt", output_dir);

    if (pack_game_data(bin_path, sprites, total_sprites,
                       (const packed_color_t (*)[PALETTE_ENTRIES])packed_pals,
                       num_sheets) != 0) {
        fprintf(stderr, "pipeline: packing failed\n");
        return -1;
    }
    printf("Wrote %s\n", bin_path);

    /* render verification image */
    if (render_ppm(bin_path, ppm_path) != 0) {
        fprintf(stderr, "pipeline: rendering failed\n");
        return -1;
    }
    printf("Wrote %s\n", ppm_path);

    /* cleanup */
    for (int i = 0; i < num_sheets; i++)
        bmp_free(&images[i]);

    printf("Pipeline complete: %d sprites from %d sheets\n",
           total_sprites, num_sheets);
    return 0;
}
