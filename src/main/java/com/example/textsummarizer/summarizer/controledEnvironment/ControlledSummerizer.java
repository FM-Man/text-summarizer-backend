package com.example.textsummarizer.summarizer.controledEnvironment;

import com.example.textsummarizer.summarizer.EigenVector;
import com.example.textsummarizer.summarizer.MatrixCalculator;
import com.example.textsummarizer.summarizer.dataset.DatasetReader;
import opennlp.tools.tokenize.WhitespaceTokenizer;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static com.example.textsummarizer.summarizer.dataset.DatasetReader.wvd;

public class ControlledSummerizer {

    private double[][] affinityMatrix = new double[][]{
            {1.00, 0.85, 0.80, 0.90, 0.25, 0.20, 0.15, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10, 0.15, 0.20},
            {0.85, 1.00, 0.90, 0.80, 0.20, 0.25, 0.20, 0.15, 0.10, 0.15, 0.10, 0.10, 0.05, 0.10, 0.05, 0.10, 0.15, 0.10, 0.10, 0.15},
            {0.80, 0.90, 1.00, 0.85, 0.15, 0.20, 0.25, 0.20, 0.10, 0.10, 0.15, 0.10, 0.05, 0.05, 0.10, 0.15, 0.10, 0.15, 0.20, 0.10},
            {0.90, 0.80, 0.85, 1.00, 0.20, 0.15, 0.20, 0.25, 0.10, 0.10, 0.10, 0.15, 0.10, 0.10, 0.05, 0.10, 0.15, 0.20, 0.10, 0.15},
            {0.25, 0.20, 0.15, 0.20, 1.00, 0.85, 0.30, 0.25, 0.20, 0.15, 0.10, 0.10, 0.05, 0.05, 0.05, 0.10, 0.10, 0.10, 0.15, 0.20},
            {0.20, 0.25, 0.20, 0.15, 0.85, 1.00, 0.90, 0.30, 0.15, 0.20, 0.15, 0.10, 0.10, 0.10, 0.05, 0.10, 0.10, 0.10, 0.10, 0.15},
            {0.15, 0.20, 0.25, 0.20, 0.30, 0.90, 1.00, 0.85, 0.10, 0.15, 0.20, 0.15, 0.05, 0.10, 0.10, 0.10, 0.10, 0.10, 0.15, 0.10},
            {0.20, 0.15, 0.20, 0.25, 0.25, 0.30, 0.85, 1.00, 0.05, 0.10, 0.15, 0.20, 0.10, 0.10, 0.05, 0.10, 0.10, 0.10, 0.10, 0.15},
            {0.15, 0.10, 0.10, 0.10, 0.20, 0.15, 0.10, 0.05, 1.00, 0.85, 0.30, 0.25, 0.20, 0.15, 0.10, 0.10, 0.10, 0.15, 0.20, 0.15},
            {0.10, 0.15, 0.10, 0.10, 0.15, 0.20, 0.15, 0.10, 0.85, 1.00, 0.90, 0.30, 0.15, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10, 0.15},
            {0.10, 0.10, 0.15, 0.10, 0.10, 0.15, 0.20, 0.15, 0.30, 0.90, 1.00, 0.85, 0.10, 0.15, 0.20, 0.15, 0.10, 0.15, 0.20, 0.10},
            {0.10, 0.10, 0.10, 0.15, 0.10, 0.10, 0.15, 0.20, 0.25, 0.30, 0.85, 1.00, 0.15, 0.10, 0.15, 0.20, 0.10, 0.10, 0.10, 0.15},
            {0.05, 0.05, 0.05, 0.10, 0.05, 0.10, 0.05, 0.10, 0.20, 0.15, 0.10, 0.15, 1.00, 0.85, 0.30, 0.25, 0.20, 0.15, 0.10, 0.10},
            {0.05, 0.10, 0.05, 0.10, 0.05, 0.10, 0.10, 0.05, 0.15, 0.20, 0.15, 0.10, 0.85, 1.00, 0.90, 0.30, 0.15, 0.20, 0.15, 0.10},
            {0.05, 0.05, 0.10, 0.05, 0.05, 0.05, 0.10, 0.15, 0.10, 0.15, 0.20, 0.15, 0.30, 0.90, 1.00, 0.85, 0.10, 0.15, 0.20, 0.15},
            {0.10, 0.10, 0.15, 0.10, 0.10, 0.10, 0.15, 0.20, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.85, 1.00, 0.15, 0.10, 0.15, 0.20},
            {0.10, 0.15, 0.10, 0.15, 0.10, 0.15, 0.10, 0.15, 0.10, 0.10, 0.10, 0.10, 0.20, 0.15, 0.10, 0.15, 1.00, 0.85, 0.30, 0.25},
            {0.10, 0.10, 0.15, 0.20, 0.10, 0.10, 0.10, 0.10, 0.15, 0.10, 0.15, 0.10, 0.15, 0.20, 0.15, 0.10, 0.85, 1.00, 0.90, 0.30},
            {0.10, 0.10, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10, 0.20, 0.15, 0.20, 0.15, 0.10, 0.15, 0.20, 0.15, 0.30, 0.90, 1.00, 0.85},
            {0.15, 0.20, 0.10, 0.15, 0.15, 0.15, 0.10, 0.15, 0.15, 0.10, 0.10, 0.15, 0.10, 0.10, 0.15, 0.20, 0.25, 0.30, 0.85, 1.00},
    };
    private double[][] degreeMatrix;
    private double[][] graphLaplacian;

    private double secondEigenValue;
    private EigenVector secondEigenVector;

    public void driver() throws Exception {

        printMatrix(affinityMatrix);
        System.out.println("=====normalized a========================================================");

        System.out.println("=============================================================");
        degreeMatrix = MatrixCalculator.getDegreeMatrix(affinityMatrix);
        printMatrix(degreeMatrix);
        System.out.println("=============================================================");
        graphLaplacian = MatrixCalculator.subtractMatrix(degreeMatrix,affinityMatrix);
        printMatrix(graphLaplacian);
        System.out.println("=============================================================");
//        graphLaplacian = MatrixCalculator.normalizeLaplacianAccordingToWikipedia(graphLaplacian);
//        printMatrix(graphLaplacian);
        secondEigenVector = MatrixCalculator.getEigenValueAndEigenVector(graphLaplacian);
//        secondEigenVector.sort();
    }




    private void printMatrix(double[][] matrix){
        for (double[] row: matrix){
            for(double cell: row){
                System.out.printf("%4.3f  ",cell);
            }
            System.out.println();
        }
    }
}
