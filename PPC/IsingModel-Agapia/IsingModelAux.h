#ifndef ISINGMODELAUX_H
#define ISINGMODELAUX_H

#include <stdio.h>

#define LATICE_DIMENSION 100
#define J 1
#define B 0
#define kT 1
#define STEPS 1000000
#define ITERATIONS 1000

class IsingModelAux
{
public:
	static int** initialization(int n);
	static int calculateEnergy(int** latice, int n);
	static int calculateEnergyDifference(int** latice, int lineIndex, int columnIndex, int n);
};

#endif