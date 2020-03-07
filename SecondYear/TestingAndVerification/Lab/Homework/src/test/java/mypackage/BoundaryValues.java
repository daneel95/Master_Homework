package mypackage;

/*
* Valori de frontiera
* Pentru N avem urmatoarele valori de frontiera
* 1. N = 0
* 2. N = 1
* 3. N = 1000
* 4. N = 1001
*
* Iesirile posibile sunt urmatoarele:
* 1. Output = 0:N
* 2. Error
*
* */

import mypackage.ArithmeticCombination;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static java.util.Collections.emptyList;
import static java.util.Collections.singletonList;
import static org.junit.Assert.assertEquals;

public class BoundaryValues {
    @Test(expected = IllegalArgumentException.class)
    public void testValueOfNIsZero() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = emptyList();
        final int inputN = 0;
        arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testValueOfNIsMoreThanMaximumAllowed() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = new ArrayList<Integer>();
        final int inputN = 1001;
        for (int i = 0; i < inputN; i++) {
            inputArray.add(i);
        }
        arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0);
    }

    @Test
    public void testValueOfNIsOne() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = singletonList(1);
        final int inputN = 1;
        assertEquals("Value should be 0", 0, arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0));
        assertEquals("Value should be 0", 1, arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 1, 0, 0));
    }

    @Test
    public void testValueOfNIsMaximum() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = new ArrayList<Integer>();
        final int inputN = 1000;
        for (int i = 0; i < inputN; i++) {
            inputArray.add(i + 1);
        }
        assertEquals("Value should be 0", 0, arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0));
        assertEquals("Value should be 0", 1, arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 1, 0, 0));
    }
}
