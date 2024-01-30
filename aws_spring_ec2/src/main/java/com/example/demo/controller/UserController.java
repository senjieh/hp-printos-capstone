package com.example.demo.controller;

import com.example.demo.model.Printer;

import com.example.demo.service.PrinterService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private PrinterService printerService;

    @GetMapping("/hello")
    public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
        return String.format("Hello %s!", name);
    }

    @GetMapping("/printers")
    public List<Printer> fetchPrinterData(@RequestParam(value = "user_id") Integer id) {
        return printerService.fetchPrintersByUserId(id);
    }

}