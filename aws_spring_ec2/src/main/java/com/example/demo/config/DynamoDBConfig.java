package com.example.demo.config;

import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class DynamoDBConfig {

    @Bean
    public DynamoDbClient dynamoDbClient() {
        return DynamoDbClient.builder()
                .region(Region.US_EAST_2) // change this to your preferred region
                .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create(
                        "AKIAYXUEF7I5BGJDG67R", "KdR5lEIlA3bn/8DgYIvfgo95t7vnGJ53iJrZShjs")))
                .build();
    }
}
