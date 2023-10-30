package com.example.demo.service;

import com.example.demo.model.Printer;
import com.example.demo.repository.PrinterRepository;

import software.amazon.awssdk.services.dynamodb.model.AttributeValue;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.time.temporal.IsoFields;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class PrinterService {

    @Autowired
    private PrinterRepository printerRepository;
    
    public List<Printer> fetchPrinterData(long start, long end, String interval, int printerId) {
        List<Map<String, AttributeValue>> rawData = printerRepository.fetchPrinterData(start, end, printerId);

        // Convert raw data to list of Printer KPIs
        List<Printer> initialData = rawData.stream().map(item -> {
            Printer printer = new Printer();
            printer.setTotalPlanned(Long.parseLong(item.get("print_job_pages").n()));
            printer.setTotalDropped(Long.parseLong(item.get("print_job_pages_dropped").n()));
            printer.setTotalPrinted(Long.parseLong(item.get("print_job_pages_printed").n()));
            printer.setTimestampStart(Long.parseLong(item.get("timestamp").n()));
            return printer;
        }).collect(Collectors.toList());

        // Group by interval
        Map<Long, List<Printer>> groupedData = new HashMap<>();
        for (Printer printer : initialData) {
            long keyTimestamp = getIntervalStartTimestamp(printer.getTimestampStart(), interval);
            groupedData.putIfAbsent(keyTimestamp, new ArrayList<>());
            groupedData.get(keyTimestamp).add(printer);
        }

        // Calculate aggregated KPIs for each interval
        List<Printer> result = new ArrayList<>();
        for (long keyTimestamp : groupedData.keySet()) {
            Printer aggregatedPrinter = new Printer();
            aggregatedPrinter.setTimestampStart(keyTimestamp);
            aggregatedPrinter.setTimestampEnd(getIntervalEndTimestamp(keyTimestamp, interval));

            for (Printer printer : groupedData.get(keyTimestamp)) {
                aggregatedPrinter.setTotalPlanned(aggregatedPrinter.getTotalPlanned() + printer.getTotalPlanned());
                aggregatedPrinter.setTotalDropped(aggregatedPrinter.getTotalDropped() + printer.getTotalDropped());
                aggregatedPrinter.setTotalPrinted(aggregatedPrinter.getTotalPrinted() + printer.getTotalPrinted());
            }

            result.add(aggregatedPrinter);
        }

        return result;
    }

    private long getIntervalStartTimestamp(long currentTimestamp, String interval) {
        LocalDateTime dateTime = LocalDateTime.ofInstant(Instant.ofEpochSecond(currentTimestamp), ZoneId.systemDefault());
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

