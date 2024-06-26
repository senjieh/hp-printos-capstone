package com.example.demo.repository;

import java.util.List;
import java.util.Map;

public interface LoginRepository {
    List<Map<String, Object>> fetchLoginData(String username, String password);

    List<Map<String, Object>> fetchGitLoginData(String username);

    Boolean registerUser(String username, String password);

    String fetchUserID(String username);

    String logSessionToken(String sessionID);
}
