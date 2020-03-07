package mypackage;

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static org.junit.Assert.assertEquals;

/**
 * The diagram of the program can be found in PROJECT_ROOT/ProgramGraph
 * There are 2 possible outcomes:
 * 1. Error (throwing exception)
 * 2. A value between 0 and 1000
 * According to the diagram there are 2 conditions that can change the outcome.
 * The first condition refers to the value of N which can be:
 * 1. N < 1
 * 2. 1 <= N <= 1000
 * 3. N > 1000
 * And the second condition refers to the size of the array which can be:
 * 1. ArraySize == N
 * 2. ArraySize != N
 *
 * According to those, the only relevant tests for MC/DC coverage are the following:
 * 1. N < 1, ArraySize == N, outcome = Error (exception)
 * 2. 1 <= N <= 1000, ArraySize == N, outcome = Number between 0 and 1000
 * 3. 1 <= N <= 1000, ArraySize != N, outcome = Error (exception)
 * 4. N > 1000, ArraySize == N, outcome = Error (exception)
 *
 * This way we get to test all the combinations that are necessary to get
 * all the possible outcomes with all the necessary input values
 */

public class MCDCTest {
    @Test(expected = IllegalArgumentException.class)
    public void test1() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 0;
        final List<Integer> array = emptyList();
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }

    @Test
    public void test2() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 10;
        final List<Integer> array = asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
        assertEquals("The result should be 0", 0, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0));
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 1, 2, 2));
    }

    @Test(expected = IllegalArgumentException.class)
    public void test3() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 10;
        final List<Integer> array = asList(1, 2, 3, 4, 5, 6);
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test4() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 1001;
        final List<Integer> array = new ArrayList<Integer>();
        for (int i = 0; i < valueOfN; i++) {
            array.add(i);
        }
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }




}
