package com.example.login.controller;

import com.example.login.model.LoginRequest;

import org.springframework.web.bind.annotation.RestController;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

/*
 * @PostMapping - does a post operation to a given path
 * login() - takes data in the format of LoginRequest object, and returns a ResponseEntity
 * 
 */
@RestController
public class LoginController {
    @PostMapping("/login")
    public ResponseEntity<?> login(@RequestBody LoginRequest loginRequest) {
        /*
         * .ok() makes the response Entity status code 200
         * .body() is the contents we return to the frontend
         */
        return ResponseEntity.ok().body("Successfully logged in"); // returned to frontend
    }
}
