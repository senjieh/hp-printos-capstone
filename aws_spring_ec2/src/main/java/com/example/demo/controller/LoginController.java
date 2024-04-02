package com.example.demo.controller;

import com.example.demo.model.LoginRequest;
import com.example.demo.service.LoginService;
import com.example.demo.service.TokenService;

import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;

import java.util.Map;

@RestController
public class LoginController {

    @Autowired
    private LoginService loginService;

    private final TokenService tokenService;

    public LoginController(TokenService tokenService) {
        this.tokenService = tokenService;
    }

    @PostMapping("/registration")
    public ResponseEntity<String> register_response(@RequestBody @Valid LoginRequest registrationRequest,
            BindingResult bindingResult) {

        if (bindingResult.hasErrors()) {
            return ResponseEntity.badRequest().body("Registration unsuccessful 1"); // get rid of 1 in body msg for demo
        }

        String username = registrationRequest.getUsername();
        String password = registrationRequest.getPassword();

        if (loginService.registerUser(username, password)) {
            return ResponseEntity.ok().body("Registration successful");
        }
        return ResponseEntity.status(401).body("Registration unsuccessful 2"); // get rid of 2 in body msg for demo
    }

    @GetMapping("/gh-oauth")
    public ResponseEntity<?> githubOAuth(@RequestParam("code") String code) {
        // String accessToken = loginService.fetchAccessToken(code);
        // if (accessToken == null) {
        // return ResponseEntity.badRequest().body("Failed to retrieve access token");
        // }

        // System.out.println(accessToken);

        // Map<String, Object> userInfo = loginService.fetchGitHubUserInfo(accessToken);
        // if (userInfo == null) {
        // return ResponseEntity.badRequest().body("Failed to retrieve user info");
        // }

        // System.out.println(userInfo);

        // String userLogin = (String) userInfo.get("login");
        // return ResponseEntity.ok().body("GitHub User Login: " + userLogin);

        // // Authenticate against database records
        // UserDetails userDetails = userDetailsService.loadUserByUsername(userLogin);
        // if (userDetails == null) {
        // return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("User does not
        // exist");
        // }

        // Programmatically authenticate the user
        Authentication authentication = new UsernamePasswordAuthenticationToken(
                "yoota", "test");
        SecurityContextHolder.getContext().setAuthentication(authentication);

        // Generate JWT token
        String jwtToken = tokenService.generateToken(authentication);

        return ResponseEntity.ok().body("JWT Token: " + jwtToken);

    }

    @PostMapping("/login")
    public ResponseEntity<String> login_response(@RequestBody @Valid LoginRequest loginRequest,
            BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return ResponseEntity.badRequest().body("Login unsuccessful 1");
        }

        String username = loginRequest.getUsername();
        String password = loginRequest.getPassword();

        if (loginService.fetchLoginData(username, password)) {
            String sessionToken = loginService.logSessionToken(username);
            return ResponseEntity.ok().body("Login Successful.\nSession Token: " + sessionToken);
        }
        return ResponseEntity.status(401).body("Login unsuccessful 2");
    }
}
