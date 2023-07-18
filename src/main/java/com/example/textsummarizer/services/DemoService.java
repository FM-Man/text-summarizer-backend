package com.example.textsummarizer.services;

import com.example.textsummarizer.models.Payload;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class DemoService {
    public Optional<Payload> summarize(Payload request){
        Payload payload = new Payload("Summarized Text of '"+request.getText()+"'");
        return Optional.of(payload);
    }
}
