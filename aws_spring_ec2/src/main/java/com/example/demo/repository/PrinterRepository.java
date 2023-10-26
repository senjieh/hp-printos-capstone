package com.example.demo.repository;


import com.example.demo.model.Printer;
import java.util.List;

public interface PrinterRepository {
    void save(Printer printer);
    Printer get(Long id);
    List<Printer> getAll();
    void delete(Long id);
}
