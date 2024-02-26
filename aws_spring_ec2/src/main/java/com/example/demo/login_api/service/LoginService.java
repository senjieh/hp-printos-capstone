package com.example.demo.login_api.service;

import com.example.demo.login_api.repository.LoginRepository;
import com.example.demo.login_api.model.LoginRequest;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service; // for @Service

import java.util.List;
import java.util.Map;
import java.util.ArrayList;

@Service
public class LoginService {
    @Autowired
    private LoginRepository loginRepository;

    public boolean registerUser(String username, String password) {
        return loginRepository.registerUser(username, password);
    }

    public boolean fetchLoginData(String username, String password) {
        List<Map<String, Object>> rawData = loginRepository.fetchLoginData(username, password);

        // TODO: include some logic that handles if there are multiple instances of a
        // user
        return (rawData.size() >= 1);
    }

    public String logSessionToken(String username) {

        String userID = loginRepository.fetchUserID(username);

        String sessionToken = loginRepository.logSessionToken(userID);

        return (sessionToken);
    }
}
