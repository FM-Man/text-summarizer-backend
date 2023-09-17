package com.example.textsummarizer.summarizer;

import java.util.ArrayList;

public class EigenVectorAndValue {
    public final ArrayList<double[]> vectors;
    public final double[] values;
    public final int[] position;

    public EigenVectorAndValue(ArrayList<double[]> vectors, double[] values) {
        this.vectors = vectors;
        this.values = values;
        position = new int[this.vectors.size()];
        for (int i = 0; i< this.vectors.size(); i++){
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
                    double[] vector = vectors.get(i);
                    vectors.set(i,vectors.get(j));
                    vectors.set(j,vector);
                    int pos = position[i];
                    position[i] = position[j];
                    position[j]=pos;
                }
            }
        }
    }

    public int getClusterNumber(){
        int pos=0;
        double differenceMax = Double.NEGATIVE_INFINITY;

        for(int i=3;i<values.length;i++){
            if(values[i]-values[i-1] > differenceMax){
                differenceMax = values[i]-values[i-1];
                pos = i;
            }
        }
        return pos;
    }

    public void printEV(){
        System.out.println("Eigenvalues:");
        for (double value : values) {
            System.out.printf("%.2f | ",value);
        }
        System.out.println();
        System.out.print("    ");
        for (int i=1;i<values.length;i++){
            System.out.printf("%.2f | ", (values[i]-values[i-1]) );
        }
    }


    public ArrayList<EigenPoint> getEigenPoints(){
        int k = getClusterNumber();
        ArrayList<EigenPoint> eigenPoints = new ArrayList<>();

        for (int i=0; i<vectors.get(0).length;i++){
            double[] point = new double[k];
            for (int j=0;j<k;j++){
                point[j] = vectors.get(j)[i];
            }
            eigenPoints.add(new EigenPoint(i,point));
        }
        return eigenPoints;
    }
}
