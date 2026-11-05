#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/wait.h>

void term_handler(int sig) {
    (void)sig;
    while (waitpid(-1, NULL, WNOHANG) > 0);
    _exit(0);
}

int main(int argc, char *argv[]) {
    int n = argc > 1 ? atoi(argv[1]) : 1;
    signal(SIGTERM, term_handler);
    for (int i = 0; i < n; i++) {
        if (fork() == 0) _exit(0);
    }
    while(1) sleep(300);
    return 0;
}
