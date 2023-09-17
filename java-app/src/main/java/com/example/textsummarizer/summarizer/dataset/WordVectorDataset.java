package com.example.textsummarizer.summarizer.dataset;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class WordVectorDataset implements Serializable {
    public HashMap<String,float[]> dataset = new HashMap<>();
}
