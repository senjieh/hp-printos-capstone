package com.example.demo.controller;

import com.example.demo.model.Printer;

import com.example.demo.service.PrinterService;
import com.example.demo.repository.PrinterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/printers")
public class PrinterController {

    @Autowired
    private PrinterService printerService;

    @GetMapping("/hello")
    public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        return String.format("Hello %s!", name);
    }

    @GetMapping("/{id}/print-data")
    public List<Printer> fetchPrinterData(@PathVariable int id, @RequestParam(value = "date_start", defaultValue = "") long start_date, @RequestParam(value = "date_end", defaultValue = "") long date_end, @RequestParam(value = "interval", defaultValue = "") String interval ) {
        return printerService.fetchPrinterData(start_date, date_end, interval, id);
    }

}
