#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N     4000000   /* 4 M elements — deliberately exceeds L3 cache */
#define REPS  5         /* repeat to stabilise timing */

static double elapsed_sec(struct timespec a, struct timespec b)
{
    return (b.tv_sec - a.tv_sec) + (b.tv_nsec - a.tv_nsec) * 1e-9;
}

int main(void)
{
    double    *x  = malloc(N * sizeof(double));
    double    *y  = malloc(N * sizeof(double));
    long long *xi = malloc(N * sizeof(long long));
    long long *yi = malloc(N * sizeof(long long));

    if (!x || !y || !xi || !yi) {
        fprintf(stderr, "malloc failed\n");
        return 1;
    }

    double    alpha = 2.718281828459045;
    long long ai    = 3;

    for (int i = 0; i < N; i++) {
        x[i]  = (double)i / N;
        y[i]  = (double)(N - i) / N;
        xi[i] = (long long)i;
        yi[i] = (long long)(N - i);
    }

    /* ---- Double-precision DAXPY ---- */
    struct timespec t0, t1;

    /* warmup pass — not timed */
    for (int i = 0; i < N; i++) y[i] += alpha * x[i];

    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int r = 0; r < REPS; r++)
        for (int i = 0; i < N; i++)
            y[i] += alpha * x[i];
    clock_gettime(CLOCK_MONOTONIC, &t1);

    double fp_sec  = elapsed_sec(t0, t1);
    double mflops  = 2.0 * N * REPS / fp_sec / 1e6;

    /* prevent dead-code elimination */
    double chk_fp = 0.0;
    for (int i = 0; i < N; i++) chk_fp += y[i];

    printf("=== Double-precision DAXPY ===\n");
    printf("N=%d  reps=%d\n", N, REPS);
    printf("Time:   %.4f s\n", fp_sec);
    printf("MFLOPS: %.1f\n", mflops);
    printf("Chk:    %.6e\n\n", chk_fp);

    /* ---- Integer DAXPY ---- */

    /* warmup */
    for (int i = 0; i < N; i++) yi[i] += ai * xi[i];

    clock_gettime(CLOCK_MONOTONIC, &t0);
    for (int r = 0; r < REPS; r++)
        for (int i = 0; i < N; i++)
            yi[i] += ai * xi[i];
    clock_gettime(CLOCK_MONOTONIC, &t1);

    double    int_sec  = elapsed_sec(t0, t1);
    double    mops_int = 2.0 * N * REPS / int_sec / 1e6;
    long long chk_int  = 0;
    for (int i = 0; i < N; i++) chk_int += yi[i];

    printf("=== Integer DAXPY ===\n");
    printf("Time:   %.4f s\n", int_sec);
    printf("MOPS:   %.1f\n", mops_int);
    printf("Chk:    %lld\n\n", chk_int);

    double ratio = mops_int / mflops;

    printf("=== Summary ===\n");
    printf("MFLOPS:                   %.1f\n", mflops);
    printf("MOPS_INT:                 %.1f\n", mops_int);
    printf("Float/Int ratio (INT/FP): %.2f\n\n", ratio);

    /* Write machine-readable results */
    FILE *f = fopen("/tmp/bench_results.txt", "w");
    if (f) {
        fprintf(f, "MFLOPS=%.1f\n",   mflops);
        fprintf(f, "MOPS_INT=%.1f\n", mops_int);
        fprintf(f, "RATIO=%.2f\n",    ratio);
        fclose(f);
        printf("Results written to /tmp/bench_results.txt\n");
    } else {
        fprintf(stderr, "Warning: could not write /tmp/bench_results.txt\n");
    }

    free(x); free(y); free(xi); free(yi);
    return 0;
}
