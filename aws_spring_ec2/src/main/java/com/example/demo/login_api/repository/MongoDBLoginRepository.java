package com.example.demo.login_api.repository;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import org.bson.Document;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Repository
public class MongoDBLoginRepository implements LoginRepository {
    @Autowired
    private MongoClient mongoClient;

    private static final String DATABASE_NAME = "hp_print_os";
    private static final String COLLECTION_NAME = "users";

    @Override
    public List<Map<String, Object>> fetchLoginData(String username, String password) {
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(COLLECTION_NAME);

        // Sanitize the user input with only alphanumerics
        // Need to parameterize the query but still don't
        // know how to do that here
        username.replaceAll("[^a-zA-Z0-9]", "");
        password.replaceAll("[^a-zA-Z0-9]", "");

        List<Map<String, Object>> results = new ArrayList<>();
        /*
         * query checking whether given username and password parameters
         * exist in our MongoDB database
         */
        collection.find(
                Filters.and(
                        Filters.eq("username", username),
                        Filters.eq("password", password)))
                .into(results);

        // System.out.println(results); // for debugging
        return results;
    }
}
