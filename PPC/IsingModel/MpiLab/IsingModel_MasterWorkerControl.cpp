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

// Returneaza laticea initializata (toate valorile 1)
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

// Returneaza energia calculata din laticea data
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

// Calculeaza diferenta dintre vechea energie si noua energie daca se modifica elementul de pe pozitia [lineIndex, columnIndex]
int calculateEnergyDifference(int** latice, int lineIndex, int columnIndex, int n) {
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

// Se face initializare globala (toate iteratiile au aceeasi initializare)
int** initialLatice = initialization(LATICE_DIMENSION);
int initialEnergy = calculateEnergy(initialLatice, LATICE_DIMENSION);

int main(int argc, char* argv[]) {
	clock_t tStart = clock();
	const int rc = MPI_Init(&argc, &argv);

	if (rc != MPI_SUCCESS) {
		printf("Failed");
		MPI_Abort(MPI_COMM_WORLD, rc);
	}

	int numProcs, rank;
	MPI_Comm_size(MPI_COMM_WORLD, &numProcs);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank);

	if (rank == 0) {
		MPI_Status status;
		int msg = 0;
		// Masterul controleaza toate iteratiile si trimite worker-ilor 
		// (cand acestia spun master-ului ca sunt liberi) mesajul de continuare (rulare de 1 step al algoritmului)
		for (int i = 1; i <= ITERATIONS; i++) {
			//printf("[MASTER] Receiving message from any1\n");
			//fflush(stdout);
			int recv = 0;
			MPI_Recv(&recv, 1, MPI_INT, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, &status);
			//printf("[MASTER] Received message %d from process number %d. So sending a message back to him.\n", recv, status.MPI_SOURCE);
			//fflush(stdout);
			msg++;
			MPI_Send(&msg, 1, MPI_INT, status.MPI_SOURCE, 1, MPI_COMM_WORLD);
			//printf("[MASTER] Master sent a message to %d\n", status.MPI_SOURCE);
			//fflush(stdout);
		}

		// Preia toate mesajele care sunt trimise de workeri (ultimele)
		// get messages from all slaves
		for (int i = 1; i < numProcs; i++) {
			//printf("Clearing the queue...\n");
			//fflush(stdout);
			int recv = 0;
			MPI_Recv(&recv, 1, MPI_INT, MPI_ANY_SOURCE, 1, MPI_COMM_WORLD, &status);
			//printf("Receiving the last message from %d \n", status.MPI_SOURCE);
			//fflush(stdout);
		}

		// Trimite un mesaj de incheiere
		msg = ITERATIONS + 1;
		for (int i = 1; i < numProcs; i++) {
			//printf("Sending termination message to slave %d \n", i);
			//fflush(stdout);
			MPI_Send(&msg, 1, MPI_INT, i, 1, MPI_COMM_WORLD);
		}
	}
	else {
		int message = 0;
		while (true) {
			//int toReceive = 0;
			MPI_Status status;
			//printf("Rank %d sending a message to master\n", rank);
			//fflush(stdout);
			MPI_Send(&rank, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
			//printf("Rank %d waiting for a message from master.\n", rank);
			//fflush(stdout);
			MPI_Recv(&message, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
			//printf("Rank %d Received a message from master (message = %d) \n", rank, message);
			//fflush(stdout);

			// opreste-te daca asa spune master-ul
			if (message > ITERATIONS)
				break;
			// Ruleaza algoritmul
			int** latice = initialLatice;
			int energy = initialEnergy;
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
			printf("Ended iteration %d with energy = %d\n", message, energy);
			fflush(stdout);
		}
	}

	MPI_Finalize();
	printf("Time taken for task %d: %.2fs\n", rank, (double)(clock() - tStart) / CLOCKS_PER_SEC);
	fflush(stdout);

	return 0;
}