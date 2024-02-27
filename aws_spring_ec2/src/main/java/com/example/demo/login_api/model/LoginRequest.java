package com.example.demo.login_api.model;

import jakarta.validation.constraints.Pattern;

public class LoginRequest {
    // state

    // Should error out and display these messages to the front end
    // somehow
    @Pattern(regexp = "^[a-zA-Z0-9]*@[a-zA-Z0-9]*\\.[a-zA-Z0-9]*$", message = "Only valid email format allowed")
    private String username;

    @Pattern(regexp = "^[a-zA-Z0-9]*$", message = "Only alphanumeric characters are allowed")
    private String password;

    // constructor
    public LoginRequest(String username, String password) {
        this.username = username;
        this.password = password;
    }

    /*
     * Getters and setters are for spring boot framework to populate and access
     * data associated with LoginRequest
     */

    // Getters
    public String getPassword() {
        return password;
    }

    public String getUsername() {
        return username;
    }

    // Setters
    public void setPassword(String password) {
        this.password = password;
    }

    public void setUsername(String username) {
        this.username = username;
    }
}
