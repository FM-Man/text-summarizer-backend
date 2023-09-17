package com.example.textsummarizer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.File;
import java.io.IOException;

import static com.example.textsummarizer.summarizer.dataset.DatasetReader.*;

@SpringBootApplication
public class TextSummarizerApplication {

	public static void main(String[] args) throws IOException, ClassNotFoundException {


		SpringApplication.run(TextSummarizerApplication.class, args);
	}

}
