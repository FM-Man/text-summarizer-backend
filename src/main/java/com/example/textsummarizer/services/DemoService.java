package com.example.textsummarizer.services;

import com.example.textsummarizer.models.Payload;
import com.example.textsummarizer.summarizer.SummarizerStartingPoint;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class DemoService {
    public Optional<Payload> summarize(Payload request){
        String summarizedText = SummarizerStartingPoint
                .getInstance()
                .driver( request.getText() );

        Payload payload = new Payload("Summarized Text of '"+summarizedText+"'");
        return Optional.of(payload);
    }
}
