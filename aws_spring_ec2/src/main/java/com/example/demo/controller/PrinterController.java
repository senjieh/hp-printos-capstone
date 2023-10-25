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

    @PostMapping
    public void create(@RequestBody Printer printer) {
        printerService.save(printer);
    }

    @GetMapping("/{id}")
    public Printer get(@PathVariable Long id) {
        return printerService.get(id);
    }

    @GetMapping("/")
    public List<Printer> getAll() {
        return printerService.getAll();
    }

    @GetMapping("/{id}/print-data")
    public Printer get_status(@PathVariable Long id) {
        return printerService.get_status(id);
    }

    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        printerService.delete(id);
    }
}
