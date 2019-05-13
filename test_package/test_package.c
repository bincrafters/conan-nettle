#include <stdio.h>
#include <stdlib.h>

#include <nettle/sha1.h>

#define BUF_SIZE 16

static void display_hex(unsigned length, uint8_t *data) {
    unsigned i;

    for (i = 0; i<length; i++) {
        printf("%02x ", data[i]);
    }

    printf("\n");
}

int main(void) {
    struct sha1_ctx ctx;
    uint8_t buffer[BUF_SIZE] = {"Bincrafters"};
    uint8_t digest[SHA1_DIGEST_SIZE] = {0};

    sha1_init(&ctx);
    sha1_update(&ctx, 12, buffer);
    sha1_digest(&ctx, SHA1_DIGEST_SIZE, digest);

    display_hex(SHA1_DIGEST_SIZE, digest);
    return EXIT_SUCCESS;
}