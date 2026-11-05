#include "hdf5.h"
#include <stdlib.h>

#define FILE_NAME  "dset.h5"
#define DATASET    "/dset"
#define NX 4
#define NY 6

int main(void) {
    hid_t   file_id, dataset_id, dataspace_id;
    hsize_t dims[2];
    herr_t  status;
    int     data[NX][NY];
    int     i, j;

    for (i = 0; i < NX; i++)
        for (j = 0; j < NY; j++)
            data[i][j] = i * NY + j;

    file_id      = H5Fcreate(FILE_NAME, H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
    dims[0]      = NX;
    dims[1]      = NY;
    dataspace_id = H5Screate_simple(2, dims, NULL);
    dataset_id   = H5Dcreate2(file_id, DATASET, H5T_NATIVE_INT, dataspace_id,
                               H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    status       = H5Dwrite(dataset_id, H5T_NATIVE_INT, H5S_ALL, H5S_ALL,
                            H5P_DEFAULT, data);
    H5Dclose(dataset_id);
    H5Sclose(dataspace_id);
    H5Fclose(file_id);
    return (int)status;
}
