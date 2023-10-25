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

@Repository
public class DynamoDBPrinterRepository implements PrinterRepository {

    @Autowired
    private DynamoDbClient dynamoDbClient;

    private static final String TABLE_NAME = "HP-capstone-dynamodb";

    @Override
    public void save(Printer printer) {
        Map<String, AttributeValue> item = new HashMap<>();
        item.put("id", AttributeValue.builder().n(String.valueOf(printer.getId())).build()); // Updated

        dynamoDbClient.putItem(PutItemRequest.builder()
                .tableName(TABLE_NAME)
                .item(item)
                .build());
    }

    @Override
    public Printer get(Long id) { // Updated type for id
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("id", AttributeValue.builder().n(String.valueOf(id)).build()); // Updated

        GetItemResponse itemResponse = dynamoDbClient.getItem(GetItemRequest.builder()
                .tableName(TABLE_NAME)
                .key(key)
                .build());

        return convertToPrinter(itemResponse.item());
    }

    @Override
    public List<Printer> getAll() {
        ScanResponse scanResponse = dynamoDbClient.scan(ScanRequest.builder()
                .tableName(TABLE_NAME)
                .build());

        List<Printer> printers = new ArrayList<>();
        for (Map<String, AttributeValue> item : scanResponse.items()) {
            printers.add(convertToPrinter(item));
        }

        return printers;
    }

    @Override
    public void delete(Long id) { // Updated type for id
        Map<String, AttributeValue> key = new HashMap<>();
        key.put("id", AttributeValue.builder().n(String.valueOf(id)).build()); // Updated

        dynamoDbClient.deleteItem(DeleteItemRequest.builder()
                .tableName(TABLE_NAME)
                .key(key)
                .build());
    }

    private Printer convertToPrinter(Map<String, AttributeValue> item) {
        Printer printer = new Printer();
        if (item != null && !item.isEmpty()) {
            if (item.containsKey("id")) {
                printer.setId(Long.parseLong(item.get("id").n()));
            }
            if (item.containsKey("brand")) {
                printer.setBrand(item.get("brand").s());
            }
            if (item.containsKey("model")) {
                printer.setModel(item.get("model").s());
            }
            if (item.containsKey("color")) {
                printer.setColor(Boolean.parseBoolean(item.get("color").bool().toString()));
            }
        }
        return printer;
    }


}
