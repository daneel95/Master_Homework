#include <stdio.h>
#include "IsingModelAux.h"
#include <string.h>
#include <assert.h>

int** IsingModelAux::initialization(int n) {
	int** latice;
	latice = new int*[n];
	for (int i = 0; i < n; i++) {
		latice[i] = new int[n];
		for (int j = 0; j < n; j++) {
			latice[i][j] = 1;
		}
	}
	return latice;
}

int IsingModelAux::calculateEnergy(int** latice, int n) {
	int energy = 0;
	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			if (i < n - 1) {
				energy += latice[i][j] * latice[i + 1][j];
			}
			if (j < n - 1) {
				energy += latice[i][j] * latice[i][j + 1];
			}
		}
	}

	return energy;
}

int IsingModelAux::calculateEnergyDifference(int** latice, int lineIndex, int columnIndex, int n) {
	int energyDifference = 0;

	if (lineIndex < n - 1) {
		energyDifference += latice[lineIndex + 1][columnIndex];
	}
	if (lineIndex > 0) {
		energyDifference += latice[lineIndex - 1][columnIndex];
	}
	if (columnIndex < n - 1) {
		energyDifference += latice[lineIndex][columnIndex + 1];
	}
	if (columnIndex > 0) {
		energyDifference += latice[lineIndex][columnIndex - 1];
	}

	return 2 * latice[lineIndex][columnIndex] * energyDifference;
}
