package com.example.demo.login_api.repository;

import java.util.List;
import java.util.Map;

public interface LoginRepository {
    // TODO: make some methods
    List<Map<String, Object>> fetchLoginData(String username, String password);

    String fetchUserID(String username);

    void logSessionToken(String sessionID);
}

