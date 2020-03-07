package mypackage;

/*
* Cauza efect
* Cauze:
* C1: N < 1
* C2: N > 1000
* C3: N = 1:1000
* C4: N = |array|
* C5: N != |array|
*
* Efecte
* E1: Error
* E2: Output = 0:N
*
* Definirea testelor folosind cauzele si avand ca expectancy efectele
* 1. C1 => E1
* 2. C2 => E1
* 3. C3 + C4 => E2
* 4. C3 + C5 => E1
* */

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static org.junit.Assert.assertEquals;

// Not the best naming :)
public class CauseEffectGraphing {
    @Test(expected = IllegalArgumentException.class)
    public void test1(){
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 0;
        final List<Integer> array = emptyList();
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }

    @Test(expected = IllegalArgumentException.class)
    public void test2(){
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 1001;
        final List<Integer> array = new ArrayList<Integer>();
        for (int i = 0; i < valueOfN; i++) {
            array.add(i);
        }

        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }

    @Test
    public void test3(){
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 10;
        // Testing when the result is 0
        final List<Integer> array = asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        assertEquals("The result should be 0", 0, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0));
        // Testing when result > 0
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 1, 2, 2));
    }

    @Test(expected = IllegalArgumentException.class)
    public void test4(){
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 10;
        final List<Integer> array = asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11);
        arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 0, 0, 0);
    }
}
