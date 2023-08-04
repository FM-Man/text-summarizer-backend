package com.example.textsummarizer.summarizer;

public class EigenVector {
    public final double[] vector;
    public final int[] position;

    public EigenVector(double[] vector) {
        this.vector = vector;
        position = new int[vector.length];
        for (int i=0; i<vector.length;i++){
            position[i] = i;
        }
    }

    public void sort(){
        for(int i=0; i< vector.length; i++){
            for (int j=0; j<i; j++){
                if(vector[i]>vector[j]){
                    double swap = vector[i];
                    vector[i] = vector[j];
                    vector[j] = swap;
                    int p = position[i];
                    position [i] = position[j];
                    position[j] =p;
                }
            }
        }
    }
}
