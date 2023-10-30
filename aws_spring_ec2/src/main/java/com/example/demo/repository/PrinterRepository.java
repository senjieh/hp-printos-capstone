package com.example.demo.repository;


import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

import java.util.List;
import java.util.Map;

public interface PrinterRepository {
    public List<Map<String, AttributeValue>> fetchPrinterData(long start, long end, int printerId) ;
}
