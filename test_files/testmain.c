

/**************************************************************************/
/*                                                                        */
/*  This file is part of FISSC.                                           */
/*                                                                        */
/*  you can redistribute it and/or modify it under the terms of the GNU   */
/*  Lesser General Public License as published by the Free Software       */
/*  Foundation, version 3.0.                                              */
/*                                                                        */
/*  It is distributed in the hope that it will be useful,                 */
/*  but WITHOUT ANY WARRANTY; without even the implied warranty of        */
/*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         */
/*  GNU Lesser General Public License for more details.                   */
/*                                                                        */
/*  See the GNU Lesser General Public License version 3.0                 */
/*  for more details (enclosed in the file LICENSE).                      */
/*                                                                        */
/**************************************************************************/


#include "testmain.h"
#include <stdio.h>

// global variables definition
BOOL g_authenticated;
SBYTE g_ptc;
UBYTE g_countermeasure;
UBYTE g_userPin[PIN_SIZE];
UBYTE g_cardPin[PIN_SIZE];
BOOL verifyPIN(void);
void initialize(void);

#ifdef INLINE
inline BOOL byteArrayCompare(UBYTE* a1, UBYTE* a2, UBYTE size) __attribute__((always_inline))
#else
BOOL byteArrayCompare(UBYTE* a1, UBYTE* a2, UBYTE size)
#endif
{
  int i;
  for(i = 0; i < size; i++) {
    if(a1[i] != a2[i]) {
      return 0;
    }
  }
  return 1;
}

#if defined INLINE && defined PTC
inline BOOL verifyPIN_0() __attribute__((always_inline))
#else
BOOL verifyPIN_0()
#endif
{
  g_authenticated = 0;

  if(g_ptc > 0) {
    if(byteArrayCompare(g_userPin, g_cardPin, PIN_SIZE) == 1) {
      g_ptc = TRIAL;
      g_authenticated = 1; // Authentication();
      return 1;
    }
    else {
      g_ptc--;
      return 0;
    }
  }

  return 1;
}

void initialize()
{
	// local variables
	int i;
	// global variables initialization
	g_authenticated = BOOL_FALSE;
	g_ptc = 3;
	g_countermeasure = 0;
	// card PIN = 1 2 3 4 5...
	for (i = 0; i < PIN_SIZE; ++i) {
		g_cardPin[i] = i+1;
	}
	// user PIN = 0 0 0 0 0...
	for (i = 0 ; i < PIN_SIZE; ++i) {
		g_userPin[i] = 0;
	}
}

void main()
{
	 initialize();
	 printf("sortie : %d\n",verifyPIN_0());
	 printf("fin\n");
}

