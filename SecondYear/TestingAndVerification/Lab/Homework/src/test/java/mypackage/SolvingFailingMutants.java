package mypackage;

import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static java.util.Arrays.asList;
import static java.util.Collections.emptyList;
import static java.util.Collections.singletonList;
import static org.junit.Assert.assertEquals;

/**
 * In acest fisier se vor omora o parte din mutantii care au supravietuit. Testul acesta va contine teste din toate
 * tipurile de teste (boundary, cause-effect si equivalence - copy pasted cele existente).
 * Se va genera un raport cu acest test folosind Pitest inainte de incercarea de omorare a mutantilor care au supravietuit
 * (adica dupa ce au fost adaugate toate testele din celelalte 3 fisiere deja existente), apoi se va face un raport
 * cu noile teste adaugate care au ca scop omorarea mutantilor care au supravietuit.
 * Noile teste vor avea in nume expresia "KillMutant" pentru a vedea care sunt testele care au fost create pentru
 * omorarea mutantilor.
 */

public class SolvingFailingMutants {
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

    // Resulted mutation coverage => 90% (26/29)
    @Test
    public void testKillMutantsThatSurvived() {
        final ArithmeticCombination arithmeticCombination = new ArithmeticCombination();
        final int valueOfN = 10;
        final List<Integer> array = asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);
        assertEquals("The result should be 4", 4, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 1, 5, 3));
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 5, 2, 4));
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 8, 1, 1));
        assertEquals("The result should be 3", 3, arithmeticCombination.calculateNumberOfCombinations(array, valueOfN, 1, 1, 8));
    }
}
