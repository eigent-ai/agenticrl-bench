# Standardization configuration
# This project uses sample standard deviation (Bessel's correction, n-1 denominator)
# for all feature scaling. R's built-in sd() function uses this convention by default.
# All scaler implementations must use sample std (n-1 denominator), NOT population std (n denominator).
STANDARDIZATION_BESSEL <- TRUE   # TRUE = use n-1 denominator (sample std)
TOLERANCE <- 1e-6
