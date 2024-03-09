package com.example.demo.service;

import com.example.demo.model.Printer;
import com.example.demo.model.PrinterKPI;
import com.example.demo.repository.PrinterRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class PrinterService {

    @Autowired
    private PrinterRepository printerRepository;

    // Helper method to safely parse Long values from Object
    private long parseLongFromObject(Object obj) {
        if (obj instanceof Number) {
            return ((Number) obj).longValue();
        } else if (obj != null) {
            return Long.parseLong(obj.toString());
        } else {
            throw new IllegalArgumentException("Null value cannot be converted to Long");
        }
    }

    // Helper method to safely parse Int values from Object
    private int parseIntFromObject(Object obj) {
        if (obj instanceof Number) {
            return ((Number) obj).intValue(); // Cast to int
        } else if (obj != null) {
            return Integer.parseInt(obj.toString()); // Parse as int
        } else {
            throw new IllegalArgumentException("Null value cannot be converted to Int");
        }
    }

    private String parseStringFromObject(Object obj) {
        if (obj != null) {
            return obj.toString(); // Convert to String
        } else {
            throw new IllegalArgumentException("Null value cannot be converted to String");
        }
    }

    public List<PrinterKPI> fetchPrinterData(long start, long end, String interval, int printerId) {
        List<Map<String, Object>> rawData = printerRepository.fetchPrinterData(start, end, printerId);

        // Convert raw data to list of Printer KPIs
        List<PrinterKPI> initialData = rawData.stream().map(item -> {
            PrinterKPI printer = new PrinterKPI();
            printer.setTotalPlanned(parseLongFromObject(item.get("print_job_pages")));
            printer.setTotalDropped(parseLongFromObject(item.get("print_job_pages_dropped")));
            printer.setTotalPrinted(parseLongFromObject(item.get("print_job_pages_printed")));
            printer.setTimestampStart(parseLongFromObject(item.get("timestamp")));
            return printer;
        }).collect(Collectors.toList());

        // Group by interval
        Map<Long, List<PrinterKPI>> groupedData = new HashMap<>();
        for (PrinterKPI printer : initialData) {
            long keyTimestamp = getIntervalStartTimestamp(printer.getTimestampStart(), interval);
            groupedData.putIfAbsent(keyTimestamp, new ArrayList<>());
            groupedData.get(keyTimestamp).add(printer);
        }

        // Calculate aggregated KPIs for each interval
        List<PrinterKPI> result = new ArrayList<>();
        for (long keyTimestamp : groupedData.keySet()) {
            PrinterKPI aggregatedPrinter = new PrinterKPI();
            aggregatedPrinter.setTimestampStart(keyTimestamp);
            aggregatedPrinter.setTimestampEnd(getIntervalEndTimestamp(keyTimestamp, interval));

            for (PrinterKPI printer : groupedData.get(keyTimestamp)) {
                aggregatedPrinter.setTotalPlanned(aggregatedPrinter.getTotalPlanned() + printer.getTotalPlanned());
                aggregatedPrinter.setTotalDropped(aggregatedPrinter.getTotalDropped() + printer.getTotalDropped());
                aggregatedPrinter.setTotalPrinted(aggregatedPrinter.getTotalPrinted() + printer.getTotalPrinted());
            }

            result.add(aggregatedPrinter);
        }

        return result; // look into how springboot is turning objects into json
    }

    private Printer convertMapToPrinter(Map<String, Object> item) {
        Printer printer = new Printer();
        printer.setID(parseIntFromObject(item.get("printer_id")));
        printer.setUserID(parseIntFromObject(item.get("user_id")));
        printer.setLastUpdate(parseIntFromObject(item.get("last_update")));
        printer.setModel(parseStringFromObject(item.get("printer_model")));
        printer.setType(parseStringFromObject(item.get("printer_type")));
        printer.setPrinterImage(parseStringFromObject(item.get("printer_image")));
        printer.setConnectionStart(parseIntFromObject(item.get("connection_start")));
        return printer;
    }

    public List<Printer> fetchPrinterByPrinterId(Integer printerId) {
        List<Map<String, Object>> rawData = printerRepository.fetchPrinterDetails(printerId);
        return rawData.stream().map(this::convertMapToPrinter).collect(Collectors.toList());
    }

    public List<Printer> fetchPrintersByUserId(Integer userId) {
        List<Map<String, Object>> rawData = printerRepository.fetchPrintersByUserId(userId);
        return rawData.stream().map(this::convertMapToPrinter).collect(Collectors.toList());
    }

    private long getIntervalStartTimestamp(long currentTimestamp, String interval) {
        LocalDateTime dateTime = LocalDateTime.ofInstant(Instant.ofEpochSecond(currentTimestamp),
                ZoneId.systemDefault());
        switch (interval) {
            case "hour":
                dateTime = dateTime.truncatedTo(ChronoUnit.HOURS);
                break;
            case "day":
                dateTime = dateTime.truncatedTo(ChronoUnit.DAYS);
                break;
            case "month":
                dateTime = dateTime.withDayOfMonth(1).truncatedTo(ChronoUnit.DAYS);
                break;
            case "year":
                dateTime = dateTime.withDayOfYear(1).truncatedTo(ChronoUnit.DAYS);
                break;
            default:
                throw new IllegalArgumentException("Invalid interval provided");
        }
        return dateTime.atZone(ZoneId.systemDefault()).toEpochSecond();
    }

    private long getIntervalEndTimestamp(long startTimestamp, String interval) {
        LocalDateTime dateTime = LocalDateTime.ofInstant(Instant.ofEpochSecond(startTimestamp), ZoneId.systemDefault());
        switch (interval) {
            case "hour":
                dateTime = dateTime.plusHours(1).minusSeconds(1); // End of the hour
                break;
            case "day":
                dateTime = dateTime.plusDays(1).minusSeconds(1); // End of the day
                break;
            case "month":
                dateTime = dateTime.plusMonths(1).minusSeconds(1); // End of the month
                break;
            case "year":
                dateTime = dateTime.plusYears(1).minusSeconds(1); // End of the year
                break;
            default:
                throw new IllegalArgumentException("Invalid interval provided");
        }
        return dateTime.atZone(ZoneId.systemDefault()).toEpochSecond();
    }

}
