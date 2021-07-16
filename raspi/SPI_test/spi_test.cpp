#include <iostream>
#include <errno.h>
#include <wiringPiSPI.h>
#include <unistd.h>

using namespace std;

static const int CHANNEL = 1;

int main()
{
   int fd, result;

   unsigned char buffer[100];

   cout << "Initializing" << endl ;

   fd = wiringPiSPISetup(CHANNEL, 1000000);

   cout << "Init result: " << fd << endl;

   unsigned char cnt = 0;
   while (1) {
           buffer[0] = cnt;
           cnt++;
           result = wiringPiSPIDataRW(CHANNEL, buffer, 1);
           cout << "result: " << result << " recieve: " << int(buffer[0]) << endl;
           usleep(100000);       // wait 10ms
   }
}
