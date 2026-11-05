#include <stdio.h>
#include <ctype.h>

int main(void) {
    int count = 0;
    int in_word = 0;
    int c;
    while ((c = getchar()) != EOF) {
        if (isspace((unsigned char)c)) {
            in_word = 0;
        } else if (!in_word) {
            in_word = 1;
            count++;
        }
    }
    printf("%d\n", count);
    return 0;
}
