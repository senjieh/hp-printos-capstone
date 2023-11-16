package com.example.demo.config;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class MongoDBConfig {

    @Bean
    public MongoClient mongoClient() {
        String connectionString = "mongodb+srv://dbuser:XSn8sDkE4xMVaDB8@printOSCluster.eucxhys.mongodb.net/?retryWrites=true&w=majority";
        return MongoClients.create(connectionString);
    }
}