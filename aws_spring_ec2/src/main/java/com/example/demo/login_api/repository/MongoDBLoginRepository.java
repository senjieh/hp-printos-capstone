package com.example.demo.login_api.repository;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Projections;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.Random;
import org.bson.Document;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.nio.charset.StandardCharsets;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;

@Repository
public class MongoDBLoginRepository implements LoginRepository {
    @Autowired
    private MongoClient mongoClient;

    private static final String DATABASE_NAME = "hp_print_os";
    private static final String COLLECTION_NAME = "users";
    private static final String COLLECTION_SESSION = "sessions";

    @Override
    public List<Map<String, Object>> fetchLoginData(String username, String password) {

        // Move this outside of this function in the future
        // Possibly have it so it tries to connect on startup
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(COLLECTION_NAME);

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

    @Override
    public String fetchUserID(String username){
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(COLLECTION_NAME);

        List<Map<String, Object>> results = new ArrayList<>();
        /*
         * query checking whether given username and password parameters
         * exist in our MongoDB database
         */
        collection.find(Filters.eq("username", username)).projection(Projections.include("_id")).into(results);

        String primaryKey = null;

        if (!results.isEmpty()) {
            Map<String, Object> document = results.get(0);
            primaryKey = document.get("_id").toString();
        }

        // System.out.println(results); // for debugging
        return primaryKey;
    }

    @Override
    public String logSessionToken(String uID){
        MongoDatabase database = mongoClient.getDatabase(DATABASE_NAME);
        MongoCollection<Document> collection = database.getCollection(COLLECTION_SESSION);

        Document document = new Document();

        try{
            SecureRandom secureRandom = SecureRandom.getInstanceStrong();
            byte[] bytes = secureRandom.generateSeed(16);
            secureRandom.nextBytes(bytes);
            String str = new String(bytes, StandardCharsets.UTF_8);
            document.append("uID", uID);
            document.append("SessionID", str);
            collection.insertOne(document);

            return(str);
           
        } catch(NoSuchAlgorithmException ex){
            Logger.getLogger(MongoDBLoginRepository.class.getName()).log(Level.SEVERE, null, ex);
        }
        
        return("Error: No Session Token was created.");

    }
}
