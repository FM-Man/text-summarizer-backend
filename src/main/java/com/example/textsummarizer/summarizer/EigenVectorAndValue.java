package com.example.textsummarizer.summarizer;

public class EigenVectorAndValue {
    public final double[][] vectors;
    public final double[] values;
    public final int[] position;

    public EigenVectorAndValue(double[][] vectors, double[] values) {
        this.vectors = vectors;
        this.values = values;
        position = new int[this.vectors.length];
        for (int i = 0; i< this.vectors.length; i++){
            position[i] = i;
        }
    }

    public void sort(){
        for(int i = 0; i< values.length; i++){
            for (int j=0; j<i; j++){
                if(values[j] > values[i]){
                    double value = values[i];
                    values[i] = values[j];
                    values[j] = value;
                    double[] vector = vectors[i];
                    vectors [i] = vectors[j];
                    vectors[j] =vector;
                }
            }
        }
    }
}
