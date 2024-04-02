package com.example.demo.service;

import com.example.demo.repository.LoginRepository;
import com.google.common.hash.Hashing;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Map;
import java.nio.charset.StandardCharsets;
import java.security.Principal;

@Service
public class LoginService {

    @Autowired
    private final LoginRepository loginRepository;

    private final WebClient webClient;

    @Value("${github.client.id}")
    private String clientId;

    @Value("${github.client.secret}")
    private String clientSecret;

    public LoginService(LoginRepository loginRepository, WebClient.Builder webClientBuilder) {
        this.loginRepository = loginRepository;
        this.webClient = webClientBuilder.build();
    }

    public boolean registerUser(String username, String password) {
        String hashedUser = Hashing.sha256()
                .hashString(username, StandardCharsets.UTF_8)
                .toString();

        String hashedPass = Hashing.sha256().hashString(password,
                StandardCharsets.UTF_8).toString();

        return loginRepository.registerUser(hashedUser, hashedPass);
    }

    public boolean fetchLoginData(String username, String password) {
        String hashedUser = Hashing.sha256()
                .hashString(username, StandardCharsets.UTF_8)
                .toString();

        String hashedPass = Hashing.sha256().hashString(password, StandardCharsets.UTF_8).toString();

        return loginRepository.fetchLoginData(hashedUser, hashedPass).size() >= 1;
    }

    public String logSessionToken(String username) {
        String userID = loginRepository.fetchUserID(username);
        return loginRepository.logSessionToken(userID);
    }

    public String fetchAccessToken(String code) {
        String accessTokenUrl = "https://github.com/login/oauth/access_token";
        Map response = webClient.post()
                .uri(accessTokenUrl)
                .header("Accept", "application/json")
                .bodyValue(Map.of(
                        "client_id", clientId,
                        "client_secret", clientSecret,
                        "code", code))
                .retrieve()
                .bodyToMono(Map.class)
                .block(); // Consider using asynchronous handling
        return (String) response.get("access_token");
    }

    public Map<String, Object> fetchGitHubUserInfo(String accessToken) {
        String userInfoUrl = "https://api.github.com/user";
        return webClient.get()
                .uri(userInfoUrl)
                .header("Authorization", "token " + accessToken)
                .retrieve()
                .bodyToMono(Map.class)
                .block(); // Consider using asynchronous handling
    }
}
