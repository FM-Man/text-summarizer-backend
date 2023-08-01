package com.example.textsummarizer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.File;
import java.io.IOException;

import static com.example.textsummarizer.summarizer.dataset.DatasetReader.*;

@SpringBootApplication
public class TextSummarizerApplication {

	public static void main(String[] args) throws IOException, ClassNotFoundException {
		File f = new File("wordVectorData.obj");
		if(f.exists()){
			System.out.println("binary dataset exists. taking input");
			objectInput();
		}
		else {
			System.out.println("binary dataset does not exists. reading from text file");
			File ft = new File("cc.bn.300.vec");
			if(ft.exists()){
				readFromTextFile();
				objectOutput();
			}
			else {
				System.out.println("dataset does not exist. please download the cc.bn.300.vec dataset (text file) from https://fasttext.cc/docs/en/crawl-vectors.html");
			}
		}

		SpringApplication.run(TextSummarizerApplication.class, args);
	}

}
