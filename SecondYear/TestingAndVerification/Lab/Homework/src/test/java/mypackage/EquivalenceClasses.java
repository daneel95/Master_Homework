package mypackage;

/*
* Clase de echivalenta
* In cazul acestei probleme exista 3 clase de echivalenta pentru intrare
* 1. N = 1:1000
* 2. N < 1
* 3. N > 1000
* Valorile lui a, b si c sunt irelevante (atata timp cat sunt intregi si a + b + c nu depaseste MAX_INT si -a-b-c nu depaseste MIN_INT)
*
* Pentru iesiri exista 2 cazuri
* 1. Aruncarea unei exceptii din cauza unei valori a lui N care nu este valida sau |array| != N
* 2. Output = 0:N <-- workflow normal
*
* Astfel vom avea urmatoarele clase de echivalenta:
* 1. N, array, a, b, c a.i. N = 1:1000, |array| = N, Output = 0:N
* 2. N, array, a, b, c a.i. N < 1, |array| = N, Output = Error
* 3. N, array, a, b, c a.i. N > 1000, |array| = N, Output = Error
* 4. N, array, a, b, c a.i. N = 1:1000, |array| != N, Output = Error
* */


import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static org.junit.Assert.assertEquals;

public class EquivalenceClasses {
    @Test
    public void testNormalFlow() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        // Testing when the result is 0
        final List<Integer> inputArray = asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        assertEquals("The result should be 0", 0, arithmeticCombination.calculateNumberOfCombinations(inputArray, 10, 0, 0, 0));
        // Testing when result > 0
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(inputArray, 10, 1, 2, 2));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNLessThanOne() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = emptyList();
        arithmeticCombination.calculateNumberOfCombinations(inputArray, 0, 0, 0, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testNGreaterThanMaximumNumber() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = new ArrayList<Integer>();
        final int inputN = 1001;
        // make sure it fails only from inputN value
        for (int i = 0; i < inputN; i++) {
            inputArray.add(1);
        }
        arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void testArraySizeDifferentThanN() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final List<Integer> inputArray = emptyList();
        final int inputN = 50;
        arithmeticCombination.calculateNumberOfCombinations(inputArray, inputN, 0, 0, 0);
    }
}
