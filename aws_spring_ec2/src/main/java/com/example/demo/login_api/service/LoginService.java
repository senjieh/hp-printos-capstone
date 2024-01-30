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

    public List<Map<String, Object>> fetchLoginData(String username, String password) {
        List<Map<String, Object>> rawData = loginRepository.fetchLoginData(username, password);

        // TODO: clean the data from database

        // Map<String, Object> element0 = rawData.get(0);
        // String usernameStr = element0.get()
        return rawData;
    }
}
