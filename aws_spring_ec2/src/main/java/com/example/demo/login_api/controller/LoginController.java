package com.example.demo.login_api.controller;

import com.example.demo.login_api.model.LoginRequest;
import com.example.demo.login_api.service.LoginService;
import com.google.common.hash.Hashing;

import jakarta.validation.Valid;

import org.springframework.web.bind.annotation.RestController;

import java.nio.charset.StandardCharsets;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;


/*
 * @PostMapping - does a post operation to a given path
 * login() - takes data in the format of LoginRequest object, and returns a ResponseEntity
 * ResponseEntities are essentially an HTTP payload that can contain status code, and a body
 */
@RestController
public class LoginController {

    @Autowired
    private LoginService loginService;

    /* @RequestBody - basically trying to get that data from frontend */
    @PostMapping("/login")
    public ResponseEntity<?> response(@RequestBody @Valid LoginRequest loginRequest, BindingResult bindingResult) {
        
        // Error on the username and passwords
        if (bindingResult.hasErrors()) {
            // Throw a bad request
            return ResponseEntity.badRequest().body("Login unsuccessful");
        }
       
        // get username and password from loginRequest
        String username = loginRequest.getUsername();
        String password = loginRequest.getPassword();

        // Hash the input to compare against database
        String hashedUser = Hashing.sha256()
        .hashString(username, StandardCharsets.UTF_8)
        .toString();
        
        String hashedPass = Hashing.sha256().
        hashString(password, StandardCharsets.UTF_8).
        toString();

        // pass username and password to LoginService
        if (loginService.fetchLoginData(hashedUser, hashedPass)) {

            //log new session in db
            loginService.logSessionToken(hashedUser);

            return ResponseEntity.ok().body("Login successful");
        }

        /*
         * .ok() makes the response Entity status code 200
         * .body() is the contents we return to the frontend
         */
        return ResponseEntity.status(401).body("Login unsuccessful");
    }
}
