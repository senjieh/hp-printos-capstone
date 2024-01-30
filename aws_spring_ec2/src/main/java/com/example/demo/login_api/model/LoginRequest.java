package com.example.demo.login_api.model;

public class LoginRequest {
    // state
    private String username;
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
