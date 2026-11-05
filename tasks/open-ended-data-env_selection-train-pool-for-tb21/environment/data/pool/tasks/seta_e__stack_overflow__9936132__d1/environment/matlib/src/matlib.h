#ifndef MATLIB_H
#define MATLIB_H

#ifndef SIZE
#define SIZE 8192
#endif

void fill_matrix(int arr[SIZE][SIZE]);
void scale_matrix(int arr[SIZE][SIZE], int factor);
long long compute_checksum(const int arr[SIZE][SIZE]);
void copy_matrix(const int src[SIZE][SIZE], int dst[SIZE][SIZE]);

#endif
