package com.example.textsummarizer.summarizer;

public class EigenPoint {
    int pos;
    double[] vector;

    public EigenPoint(int pos, double[] vector){
        this.pos = pos;
        this.vector = vector;
    }

    public int getPos() {
        return pos;
    }

    public void setPos(int pos) {
        this.pos = pos;
    }

    public double[] getVector() {
        return vector;
    }

    public void setVector(double[] vector) {
        this.vector = vector;
    }
}
