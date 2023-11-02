package com.example.demo.repository;

import com.example.demo.model.Printer;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Collections;


@Repository
public class DynamoDBPrinterRepository implements PrinterRepository {

    @Autowired
    private DynamoDbClient dynamoDbClient;

    private static final String TABLE_NAME = "HP-capstone-dynamodb";

    @Override
    public List<Map<String, AttributeValue>> fetchPrinterData(long start, long end, int printerId) {
        // Construct the ScanRequest with filters for timestamp and printer ID
        ScanRequest scanRequest = ScanRequest.builder()
            .tableName(TABLE_NAME)
            .filterExpression("(#ts BETWEEN :start AND :end) AND #pid = :printerId")
            .expressionAttributeNames(Map.of(
                "#ts", "timestamp",
                "#pid", "printer_id"  // Mapping placeholder to actual key name
            ))
            .expressionAttributeValues(Map.of(
                ":start", AttributeValue.builder().n(String.valueOf(start)).build(),
                ":end", AttributeValue.builder().n(String.valueOf(end)).build(),
                ":printerId", AttributeValue.builder().n(String.valueOf(printerId)).build()
            ))
            .build();
    
        ScanResponse scanResponse = dynamoDbClient.scan(scanRequest);
    
        // Print the raw response from DynamoDB for debugging purposes.
        System.out.println("Raw DynamoDB Response: " + scanResponse);
        
        return scanResponse.items();
    }
    


}
