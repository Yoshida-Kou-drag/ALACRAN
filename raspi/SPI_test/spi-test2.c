#include <linux/spi/spidev.h>
#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#define HOGE_SPI_SPEED_HZ    1000000
#define HOGE_SPI_DELAY_USECS 0
#define HOGE_SPI_BITS        8
#define ARRAY_SIZE(a) (sizeof(a) / sizeof((a)[0]))

int main(int argc, char *argv[])
{
    int ret;
    int fd;

    // uint8_t tx[3] = {1, 2, 3};
    uint8_t tx[1] = {2};
    uint8_t rx[3] = {0, };
    struct spi_ioc_transfer tr[1];

    tr[0].tx_buf        = (unsigned long)tx;
    tr[0].rx_buf        = (unsigned long)rx;
    tr[0].len           = ARRAY_SIZE(tx);
    tr[0].delay_usecs   = HOGE_SPI_DELAY_USECS;
    tr[0].speed_hz      = HOGE_SPI_SPEED_HZ;
    tr[0].bits_per_word = HOGE_SPI_BITS;
    tr[0].cs_change     = 0;
    ret = ioctl(fd, SPI_IOC_WR_MODE, SPI_MODE_3);
    int ret2 = ioctl(fd, SPI_IOC_MESSAGE(1), tr);
    printf("result %d %d\n",ret,ret2);
    printf("rxdata = %d\n",rx[0]);
return 0;
}
