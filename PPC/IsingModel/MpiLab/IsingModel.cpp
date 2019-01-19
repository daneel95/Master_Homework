#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/*
Cum J = 1 atunci formula energiei devine Suma dupa i si j din sigma(i) * sigma(j)
*/

#define LATICE_DIMENSION 100
#define J 1
#define B 0
#define kT 1
#define STEPS 1000000
#define ITERATIONS 1000

int** initialization(int n) {

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

int calculateEnergy(int** latice, int n) {
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

int calculateEnergyDifference(int** latice, int lineIndex, int columnIndex, int n) {
	int energyDifference = 0;

	if (lineIndex < n - 1){
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


int main(int argc, char* argv[]) {
	clock_t tStart = clock();
	const int rc = MPI_Init(&argc, &argv);

	if (rc != MPI_SUCCESS) {
		printf("Failed");
		MPI_Abort(MPI_COMM_WORLD, rc);
	}

	int numtasks, rank;
	MPI_Comm_size(MPI_COMM_WORLD, &numtasks);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	int iterationsPerTask = ITERATIONS / numtasks;
/*
	int** latice = initialization(LATICE_DIMENSION);
	for (int i = 0; i < LATICE_DIMENSION; i++) {
		for (int j = 0; j < LATICE_DIMENSION; j++) {
			printf("%d ", latice[i][j]);
		}
		printf("\n");
	}
*/
	for (int j = 0; j < iterationsPerTask; j++) {
		int** latice = initialization(LATICE_DIMENSION);
		int energy = calculateEnergy(latice, LATICE_DIMENSION);

		for (int i = 0; i < STEPS; i++) {
			int lineIndex = rand() % LATICE_DIMENSION;
			int columnIndex = rand() % LATICE_DIMENSION;
			float randomProbability = ((double)rand() / (RAND_MAX));
			float probability = 0.0f;

			int energyDifference = calculateEnergyDifference(latice, lineIndex, columnIndex, LATICE_DIMENSION);
			if (energyDifference < 0) {
				probability = 1.0;
			}
			else {
				probability = exp(-energyDifference);
			}

			if (randomProbability < probability) {
				latice[lineIndex][columnIndex] *= -1;
				energy -= energyDifference;
			}
		}

		printf("Ended iteration %d with energy = %d\n", rank * iterationsPerTask + j, energy);
	}

	MPI_Finalize();
	printf("Time taken for task %d: %.2fs\n", rank,(double)(clock() - tStart) / CLOCKS_PER_SEC);

	return 0;
}