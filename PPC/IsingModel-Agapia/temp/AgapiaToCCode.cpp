#include "AgapiaToCCode.h"
#include "ExecutionBlackbox.h"
#include "InputTypes.h"

#include "Includes.h"


void COMPUTEITERATION(InputBlock* pNorth, InputBlock* pWest, InputBlock* pSouth, InputBlock* pEast)
{
	// Local variables declaration: 
	int& iteration = ((IntDataItem*)((SimpleProcessItem*)pNorth->m_InputsInBlock[0])->m_InputItems[0])->GetValueRef();


	// User code: 
		int** latice = IsingModelAux::initialization(LATICE_DIMENSION);
		int energy = IsingModelAux::calculateEnergy(latice, LATICE_DIMENSION);
	
		for (int i = 0; i < STEPS; i++) {
			int lineIndex = rand() % LATICE_DIMENSION;
			int columnIndex = rand() % LATICE_DIMENSION;
			float randomProbability = ((double)rand() / (RAND_MAX));
			float probability = 0.0f;
	
			int energyDifference = IsingModelAux::calculateEnergyDifference(latice, lineIndex, columnIndex, LATICE_DIMENSION);
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
	
		printf("Ended iteration %d with energy = %d\n", iteration, energy);
		fflush(stdout);
	
	

}




void I(InputBlock* pNorth, InputBlock* pWest, InputBlock* pSouth, InputBlock* pEast)
{
	// Local variables declaration: 
	int& n = ((IntDataItem*)((SimpleProcessItem*)pNorth->m_InputsInBlock[0])->m_InputItems[0])->GetValueRef();


	// User code: 
	
	

}




void PREPAREDATA(InputBlock* pNorth, InputBlock* pWest, InputBlock* pSouth, InputBlock* pEast)
{
	// Local variables declaration: 
	int& iterations = ((IntDataItem*)((SimpleProcessItem*)pSouth->m_InputsInBlock[0])->m_InputItems[0])->GetValueRef();
	VectorProcessItem& tasks = *((VectorProcessItem*)pSouth->m_InputsInBlock[1]);


	// User code: 
		ClearVectorOfProcessItems(&tasks);
		iterations = ITERATIONS;
	
		for (int i = 0; i < iterations; i++){
		SetInputItemToVector(16, &tasks, i, "iteration", i);
		}
	
	

}


void InitializeAgapiaToCFunctions()
{
ExecutionBlackbox::Get()->AddAgapiaToCFunction("COMPUTEITERATION", &COMPUTEITERATION);
ExecutionBlackbox::Get()->AddAgapiaToCFunction("I", &I);
ExecutionBlackbox::Get()->AddAgapiaToCFunction("PREPAREDATA", &PREPAREDATA);
}
