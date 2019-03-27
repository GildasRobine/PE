#ifndef __TYPE__
#define __TYPE__

#define BOOL_TRUE 0xAA
#define BOOL_FALSE 0x55
#define PIN_SIZE 4
#define TRIAL 20

typedef signed char SBYTE;
typedef unsigned char UBYTE;
typedef unsigned char BOOL;
typedef unsigned long ULONG;

BOOL verifyPIN_0(void);
BOOL verifyPIN_1(void);
BOOL verifyPIN_2(void);
BOOL verifyPIN_3(void);
BOOL verifyPIN_4(void);
BOOL verifyPIN_5(void);
BOOL verifyPIN_6(void);
BOOL verifyPIN_7(void);

void initialize(void);
void trigger_up(void);
void trigger_down(void);


#endif
