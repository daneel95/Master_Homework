package mypackage;

import java.util.List;

import static java.util.Arrays.asList;

/**
 * Given an array of N elements, a value N (with 0 < N < 1000) and 3 numbers a, b and c.
 * Calculates the number of Arithmetic Combinations present in the array using number a, b and c.
 */

public class ArithmeticCombination {
    private static final int MAXIMUM_NUMBER = 1000;
    public int calculateNumberOfCombinations(List<Integer> array, int n, int a, int b, int c) {
        // validate that 0 < n < 1000
        if (n < 1 || n > MAXIMUM_NUMBER) {
            throw new IllegalArgumentException("Value of N should be between 1 and " + MAXIMUM_NUMBER);
        }

        // validate that the array has a proper size
        if (array.size() != n) {
            throw new IllegalArgumentException(String.format("The array should have the same size as the value of n. Found size = %d and n = %d", array.size(), n));
        }

        // calculate possible arithmetic combinations
        final List<Integer> combinations = calculateArithmeticCombinations(a, b, c);
        int numberOfCombination = 0;
        for (int value : array) {
            if (combinations.contains(value)) {
                numberOfCombination++;
            }
        }

        return numberOfCombination;
    }

    private List<Integer> calculateArithmeticCombinations(int a, int b, int c) {
        // calculate all possible values
        return asList(
                a + b + c,
                a + b - c,
                a - b + c,
                a - b - c,
                -a + b + c,
                -a + b - c,
                -a - b + c,
                -a - b - c);
    }
}
