package com.example.demo.service;

import com.example.demo.model.Printer;
import com.example.demo.repository.PrinterRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class PrinterService {

    @Autowired
    private PrinterRepository printerRepository;

    public void save(Printer printer) {
        printerRepository.save(printer);
    }

    public Printer get(Long id) {
        return printerRepository.get(id);
    }

    public List<Printer> getAll() {
        return printerRepository.getAll();
    }

    public void delete(Long id) {
        printerRepository.delete(id);
    }
}
