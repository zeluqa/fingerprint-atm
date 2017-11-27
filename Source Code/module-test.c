#include <windows.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

//void print_hex(const char *s)
void print_hex(char arr[], int n)
{
	// while(*s)
		// printf("%02x", ((unsigned int) *s++) & 0xff);
	// printf("\n");
	
	int i;

	for (int i = 0; i <= n; i++) {
		printf("%02x", arr[i] & 0xff);
		//printf(" %x", arr[i]);
		//printf(" %d\n", i);
	}
	putchar('\n');
}

int main()
{	
    // Define the five bytes to send ("hello")
    unsigned char bytes_to_send[20] = {0xef, 0x01, 0xff, 0xff, 0xff, 0xff, 0x01, 0x00,
	0x04, 0x17, 0x00, 0x00, 0x1c};
    // bytes_to_send[0] = 0xef;
    // bytes_to_send[1] = 0x01;
    // bytes_to_send[2] = 0xff;
    // bytes_to_send[3] = 0xff;
    // bytes_to_send[4] = 0xff;
	// bytes_to_send[5] = 0xff;
	// bytes_to_send[6] = 0x01;
	// bytes_to_send[7] = 0x00;
	// bytes_to_send[8] = 0x04;
	// bytes_to_send[9] = 0x17;
	// bytes_to_send[10] = 0x00;
	// bytes_to_send[11] = 0x00;
	// bytes_to_send[12] = 0x1c;
		
	char bytes_to_read[200];
 
    // Declare variables and structures
	int i;
	FILE *fp;
	int c;
    HANDLE hSerial;
    DCB dcbSerialParams = {0};
    COMMTIMEOUTS timeouts = {0};
         
    // Open the highest available serial port number
    fprintf(stderr, "Opening serial port...");
    hSerial = CreateFile(
                "\\\\.\\COM3", GENERIC_READ|GENERIC_WRITE, 0, NULL,
                OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL );
    if (hSerial == INVALID_HANDLE_VALUE)
    {
            fprintf(stderr, "Error\n");
            return 1;
    }
    else fprintf(stderr, "OK\n");
     
    // Set device parameters (57600 baud, 1 start bit,
    // 1 stop bit, no parity)
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    if (GetCommState(hSerial, &dcbSerialParams) == 0)
    {
        fprintf(stderr, "Error getting device state\n");
        CloseHandle(hSerial);
        return 1;
    }
     
    dcbSerialParams.BaudRate = CBR_57600;
    dcbSerialParams.ByteSize = 8;
    dcbSerialParams.StopBits = ONESTOPBIT;
    dcbSerialParams.Parity = NOPARITY;
    if(SetCommState(hSerial, &dcbSerialParams) == 0)
    {
        fprintf(stderr, "Error setting device parameters\n");
        CloseHandle(hSerial);
        return 1;
    }
 
    // Set COM port timeout settings
    timeouts.ReadIntervalTimeout = 50;
    timeouts.ReadTotalTimeoutConstant = 50;
    timeouts.ReadTotalTimeoutMultiplier = 10;
    timeouts.WriteTotalTimeoutConstant = 50;
    timeouts.WriteTotalTimeoutMultiplier = 10;
    if(SetCommTimeouts(hSerial, &timeouts) == 0)
    {
        fprintf(stderr, "Error setting timeouts\n");
        CloseHandle(hSerial);
        return 1;
    }
 
	//Communicate Link
	//Read system parameter
	
	//Part 1
	//Collect finger image
	//Upload image
	
	//Part 2
	//Download image
	//Generate character file
	//Generate template
	
	//Part 3
	//Download template
 
    // Send specified text (remaining command line arguments)
    DWORD bytes_written, total_bytes_written = 0;
    // fprintf(stderr, "Sending bytes...");
	// printf("%x\n", &bytes_to_send);
    if(!WriteFile(hSerial, bytes_to_send, 13, &bytes_written, NULL))
    {
        fprintf(stderr, "Error\n");
        CloseHandle(hSerial);
        return 1;
    }
    // fprintf(stderr, "%d bytes written\n", bytes_written);
    
	// Read
    DWORD bytes_read, total_bytes_read = 0;
    //fprintf(stderr, "Receiving bytes...\n");
    if(!ReadFile(hSerial, &bytes_to_read, 20, &bytes_read, NULL))
    {
        fprintf(stderr, "Error\n");
        CloseHandle(hSerial);
        return 1;
    }
	// fprintf(stderr, "%c\n", bytes_to_read);
	print_hex(bytes_to_send, 13);
	print_hex(bytes_to_read, bytes_read);
    fprintf(stderr, "%d bytes read\n", bytes_read);
	
	// Write to file
	// fp = fopen("test.txt","w");
	// fprintf(fp, "%d\n", bytes_read);
	// fprintf(fp, "%s\n", bytes_to_read);
	// fclose(fp);
	
    // Close serial port
    fprintf(stderr, "Closing serial port...");
    if (CloseHandle(hSerial) == 0)
    {
        fprintf(stderr, "Error\n");
        return 1;
    }
    fprintf(stderr, "OK\n");
 
    // exit normally
    return 0;
}