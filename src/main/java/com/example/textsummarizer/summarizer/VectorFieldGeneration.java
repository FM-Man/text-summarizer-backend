package com.example.textsummarizer.summarizer;

import java.util.ArrayList;
import java.util.HashMap;

public class VectorFieldGeneration {
    public static ArrayList<float[]> getVectorField(ArrayList<ArrayList<String>> sentenceDividedIntoWords){
        ArrayList<float[]> vectorField = new ArrayList<>();
        for (int i = 0; i<sentenceDividedIntoWords.size();i++){
            float[] indSentenceVectorField = new float[301];
            int totalWordsInTheSentence = sentenceDividedIntoWords.get(i).size();
            for (int j=0;j<sentenceDividedIntoWords.get(i).size();j++){
                float[] indWordVectorField = DemoDriver.wvd.dataset.get(sentenceDividedIntoWords.get(i).get(j));
                for (int k=0; k<300;k++){
                    indSentenceVectorField[k] += (1.0/totalWordsInTheSentence) * indWordVectorField[k];
                }
            }
            indSentenceVectorField[300] = (float) (i /sentenceDividedIntoWords.size());

            vectorField.add(indSentenceVectorField);
        }
        return vectorField;
    }
}
