package com.example.demo.repository;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import org.bson.Document;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Repository
public class MongoDBPrinterRepository implements PrinterRepository {

    @Autowired
    private MongoClient mongoClient;

    private static final String DATABASE_NAME = "hp_print_os";
    private static final String COLLECTION_NAME = "printer_data";
    private static final String PRINTERS_COLLECTION_NAME = "printers";

    @Override
    public List<Map<String, Object>> fetchPrinterData(long start, long end, int printerId) {
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(COLLECTION_NAME);

        // Construct the query with filters for timestamp and printer ID
        List<Map<String, Object>> results = new ArrayList<>();
        collection.find(
            Filters.and(
                Filters.gte("timestamp", start),
                Filters.lte("timestamp", end),
                Filters.eq("printer_id", printerId)
            )
        ).into(results);


        System.out.println(results);
        return results;
    }


    @Override
    public List<Map<String, Object>> fetchPrinterDetails(int printerId) {
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(PRINTERS_COLLECTION_NAME);

        // Construct the query with filters for timestamp and printer ID
        List<Map<String, Object>> results = new ArrayList<>();
        collection.find(
            Filters.and(
                Filters.eq("printer_id", printerId)
            )
        ).into(results);


        return results;
    }

    @Override
    public List<Map<String, Object>> fetchPrintersByUserId(Integer userId) {

        
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> printerCollection = database.getCollection(PRINTERS_COLLECTION_NAME);

        List<Map<String, Object>> printers = new ArrayList<>();
        List<Integer> printerIds = new ArrayList<>();

        // Fetch printer IDs associated with the user ID
        printerCollection.find(Filters.eq("user_id", userId))
            .forEach(document -> printerIds.add(document.getInteger("printer_id")));

        // Fetch printer data for each printer ID
        for (int printerId : printerIds) {
            printerCollection.find(Filters.eq("printer_id", printerId))
                .into(printers);
        }

        System.out.println(printers);

        return printers;
    }
}
