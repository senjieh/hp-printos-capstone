package com.example.demo.login_api.controller;

import com.example.demo.login_api.model.LoginRequest;
//import com.example.demo.login_api.model.RegistrationRequest;
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

    @PostMapping("/registration")
    public ResponseEntity<String> register_reponse(@RequestBody @Valid LoginRequest registrationRequest,
            BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            // Throw a bad request
            return ResponseEntity.badRequest()
                    .body("Registeration unsuccessful");
        }

        String username = registrationRequest.getUsername();
        String password = registrationRequest.getPassword();

        // Hashing should be in service layer because it's business logic

        // Hash the input
        String hashedUser = Hashing.sha256()
                .hashString(username, StandardCharsets.UTF_8)
                .toString();

        String hashedPass = Hashing.sha256().hashString(password, StandardCharsets.UTF_8).toString();

        if (loginService.registerUser(hashedUser, hashedPass)) {

            // log new session in db
            // String sessionToken = loginService.logSessionToken(hashedUser);
            // String returnString = "Successful Login.\nSession Token: " + sessionToken;

            return ResponseEntity.ok().body("Registration successful");
        }
        // 403 is forbidden
        // 401 is
        return ResponseEntity.status(401).body("Registration unsuccessful");
    }

    /* Paths should named after resources / nouns */
    @PostMapping("/login")
    /*
     * @RequestBody - basically trying to get that data from frontend
     * BindingResult -
     */
    public ResponseEntity<String> login_response(@RequestBody @Valid LoginRequest loginRequest,
            BindingResult bindingResult) {

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

        String hashedPass = Hashing.sha256().hashString(password, StandardCharsets.UTF_8).toString();

        // pass username and password to LoginService
        if (loginService.fetchLoginData(hashedUser, hashedPass)) {

            // log new session in db
            String sessionToken = loginService.logSessionToken(hashedUser);
            String returnString = "Successful Login.\nSession Token: " + sessionToken;

            // save the session token in header instead of body
            return ResponseEntity.ok().body(returnString);
        }

        /*
         * .ok() makes the response Entity status code 200
         * .body() is the contents we return to the frontend
         */
        return ResponseEntity.status(401).body("Login unsuccessful");
    }
}
