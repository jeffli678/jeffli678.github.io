#include <stdint.h>
#include <stdio.h>
#include <string.h>

void encrypt (uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0, i;           /* set up */
    uint32_t delta=0xe09ffbb1;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        sum += delta;
        v0 += ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        if (i == 22)
            v1 += ((v0<<2) + k2) ^ (v0 + sum) ^ ((v0>>3) + k3);
        else
            v1 += ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);
        printf("value after round: %d, v0: 0x%x, v1: 0x%x\n", i, v0, v1);
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}

void decrypt (uint32_t v[2], const uint32_t k[4]) {
    uint32_t v0=v[0], v1=v[1], sum=0xe09ffbb1 * 32, i;  /* set up; sum is 32*delta */
    uint32_t delta=0xe09ffbb1;                     /* a key schedule constant */
    uint32_t k0=k[0], k1=k[1], k2=k[2], k3=k[3];   /* cache key */
    for (i=0; i<32; i++) {                         /* basic cycle start */
        if (i == 9)
            v1 -= ((v0<<2) + k2) ^ (v0 + sum) ^ ((v0>>3) + k3);
        else
            v1 -= ((v0<<4) + k2) ^ (v0 + sum) ^ ((v0>>5) + k3);

        v0 -= ((v1<<4) + k0) ^ (v1 + sum) ^ ((v1>>5) + k1);
        sum -= delta;
    }                                              /* end cycle */
    v[0]=v0; v[1]=v1;
}


int main()
{
    uint32_t key[4] = {0x80b86e21, 0xa268295d, 0xf171f22d, 0x28a13c94};
    uint32_t encrypted[2] = {0xfb987633, 0xa2500488};
    decrypt(encrypted, key);
    printf("0x%x\n", encrypted[0]);
    printf("0x%x\n", encrypted[1]);
    char* buffer = malloc(9);
    memcpy(buffer, (char*)encrypted, 8);
    printf("%s\n", buffer);
    free(buffer);

    encrypted[0] = 0x6ce7082d;
    encrypted[1] = 0xc03a492f;
    decrypt(encrypted, key);
    printf("0x%x\n", encrypted[0]);
    printf("0x%x\n", encrypted[1]);
    buffer = malloc(9);
    memcpy(buffer, (char*)encrypted, 8);
    printf("%s\n", buffer);
    free(buffer);

    printf("test encrypt\n");
    // "12345678"
    uint32_t input[2] = { 0x34333231, 0x38373635};
    encrypt(input, key);
    printf("0x%x\n", input[0]);
    printf("0x%x\n", input[1]);
    decrypt(input, key);
    printf("0x%x\n", input[0]);
    printf("0x%x\n", input[1]);
    return 0;
}


// xNVa2_N07_t3aAlg

// test encrypt
// value after round: 0, v0: 0xed0835ca, v1: 0x748b3829
// value after round: 1, v0: 0x47b491ee, v1: 0xc31cb1a7
// value after round: 2, v0: 0xc6b2b4af, v1: 0xddf5fa8d
// value after round: 3, v0: 0x6fecdb40, v1: 0xc69c9d4
// value after round: 4, v0: 0xfa04a3c3, v1: 0x9538bab
// value after round: 5, v0: 0xf455407d, v1: 0x47e6c574
// value after round: 6, v0: 0x2c1a7e1f, v1: 0x114860e3
// value after round: 7, v0: 0x4d9eac7d, v1: 0xc41462f2
// value after round: 8, v0: 0xe61199b, v1: 0xceab9f5b
// value after round: 9, v0: 0x65a5ab5e, v1: 0x1a92e106
// value after round: 10, v0: 0xb14dbaa3, v1: 0x8ade9e10
// value after round: 11, v0: 0x4b90f5d3, v1: 0xde4ae710
// value after round: 12, v0: 0xd5e7e68c, v1: 0x3cf276bc
// value after round: 13, v0: 0x440a4525, v1: 0xd11038cf
// value after round: 14, v0: 0x72eed41, v1: 0x4d451232
// value after round: 15, v0: 0xadcdfb2e, v1: 0xa4d8d190
// value after round: 16, v0: 0x9481dbc7, v1: 0x10c448f7
// value after round: 17, v0: 0x86932923, v1: 0x3867d30c
// value after round: 18, v0: 0xcdeca15e, v1: 0xbf48b91e
// value after round: 19, v0: 0x64daaf34, v1: 0xa4d76786
// value after round: 20, v0: 0xdd31be47, v1: 0x462de75d
// value after round: 21, v0: 0xb214b23c, v1: 0x9868c17
// v1 is different from here
// value after round: 22, v0: 0x3e880d0e, v1: 0xa906a21b
// it starts to be different from here
// value after round: 23, v0: 0x4d1cf81d, v1: 0x5d5e6937
// value after round: 24, v0: 0xc4ed8d4, v1: 0xc2110a61
// value after round: 25, v0: 0xa83018ae, v1: 0xe40f735d
// value after round: 26, v0: 0xa4fa10bc, v1: 0x1d11dff0
// value after round: 27, v0: 0x111c2ed, v1: 0xd5c8800f
// value after round: 28, v0: 0x34cfc43d, v1: 0x888f4811
// value after round: 29, v0: 0xa91e4ea0, v1: 0xddf0868b
// value after round: 30, v0: 0x90e5ca5a, v1: 0xf494406d
// value after round: 31, v0: 0xfc48d376, v1: 0x89c923a1
// value after round: 32, v0: 0xc1dd22af, v1: 0x2151cfd5


// test encrypt
// value after round: 0, v0: 0xed0835ca, v1: 0x748b3829
// value after round: 1, v0: 0x47b491ee, v1: 0xc31cb1a7
// value after round: 2, v0: 0xc6b2b4af, v1: 0xddf5fa8d
// value after round: 3, v0: 0x6fecdb40, v1: 0xc69c9d4
// value after round: 4, v0: 0xfa04a3c3, v1: 0x9538bab
// value after round: 5, v0: 0xf455407d, v1: 0x47e6c574
// value after round: 6, v0: 0x2c1a7e1f, v1: 0x114860e3
// value after round: 7, v0: 0x4d9eac7d, v1: 0xc41462f2
// value after round: 8, v0: 0xe61199b, v1: 0xceab9f5b
// value after round: 9, v0: 0x65a5ab5e, v1: 0x1a92e106
// value after round: 10, v0: 0xb14dbaa3, v1: 0x8ade9e10
// value after round: 11, v0: 0x4b90f5d3, v1: 0xde4ae710
// value after round: 12, v0: 0xd5e7e68c, v1: 0x3cf276bc
// value after round: 13, v0: 0x440a4525, v1: 0xd11038cf
// value after round: 14, v0: 0x72eed41, v1: 0x4d451232
// value after round: 15, v0: 0xadcdfb2e, v1: 0xa4d8d190
// value after round: 16, v0: 0x9481dbc7, v1: 0x10c448f7
// value after round: 17, v0: 0x86932923, v1: 0x3867d30c
// value after round: 18, v0: 0xcdeca15e, v1: 0xbf48b91e
// value after round: 19, v0: 0x64daaf34, v1: 0xa4d76786
// value after round: 20, v0: 0xdd31be47, v1: 0x462de75d
// value after round: 21, v0: 0xb214b23c, v1: 0x9868c17
// value after round: 22, v0: 0x3e880d0e, v1: 0xc08e3dbc
// value after round: 23, v0: 0x2d05120d, v1: 0x985d1b38
// value after round: 24, v0: 0x5362ae23, v1: 0xe7ffdf6c
// value after round: 25, v0: 0x6483d202, v1: 0xea90801
// value after round: 26, v0: 0xdaa0de02, v1: 0x4e330065
// value after round: 27, v0: 0xf32410d2, v1: 0xe55e3ade
// value after round: 28, v0: 0x1b96cbab, v1: 0xf3734b72
// value after round: 29, v0: 0x7772f874, v1: 0x8243257a
// value after round: 30, v0: 0x2ea51114, v1: 0x1615136c
// value after round: 31, v0: 0x99ab0da9, v1: 0x22fbede1