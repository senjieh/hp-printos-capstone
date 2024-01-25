package com.example.login.model;

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
     * Need getters and setters for spring boot framework to populate and access
     * data associate with LoginRequest
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
