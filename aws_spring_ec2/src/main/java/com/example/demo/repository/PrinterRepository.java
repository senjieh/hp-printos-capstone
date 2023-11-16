package com.example.demo.repository;

import java.util.List;
import java.util.Map;

public interface PrinterRepository {
    List<Map<String, Object>> fetchPrinterData(long start, long end, int printerId);
    List<Map<String, Object>> fetchPrintersByUserId(Integer userId);
    List<Map<String, Object>> fetchPrinterDetails(int printerId);
}
