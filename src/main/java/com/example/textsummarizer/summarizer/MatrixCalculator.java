package com.example.textsummarizer.summarizer;

import java.util.ArrayList;

import static java.lang.Math.*;

public class MatrixCalculator {
    public static double[][] getAffinityMatrix(ArrayList<float[]> vectorField){
        double[][] affinityMatrix = new double[vectorField.size()][vectorField.size()];

        double sigma = 10;
        for (int i=0; i<vectorField.size();i++){
            for(int j=0;j<vectorField.size();j++){
                affinityMatrix[i][j] =
                        exp(
                                -1 * pow(
                                        distance(vectorField.get(i), vectorField.get(j)),
                                        2
                                ) / sigma
                        );
            }
        }

        return affinityMatrix;
    }

    private static double distance(float[] a, float[] b){
        double sumOfSquare = 0;
        for (int i=0; i<a.length;i++){
            sumOfSquare += pow(a[i]-b[i],2);
        }
        return sqrt(sumOfSquare);
    }
}
