package com.example.demo.controller;

import com.example.demo.model.LoginRequest;
import com.example.demo.service.LoginService;
import com.example.demo.service.TokenService;

import com.google.common.hash.Hashing;
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



import java.nio.charset.StandardCharsets;
import java.util.Map;

@RestController
public class LoginController {

    @Autowired
    private LoginService loginService;

    private final TokenService tokenService;
    
    public LoginController(TokenService tokenService){
        this.tokenService = tokenService;
    }

    @PostMapping("/registration")
    public ResponseEntity<String> register_response(@RequestBody @Valid LoginRequest registrationRequest,
                                                    BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return ResponseEntity.badRequest().body("Registration unsuccessful");
        }

        String username = registrationRequest.getUsername();
        String password = registrationRequest.getPassword();

        String hashedUser = Hashing.sha256()
                .hashString(username, StandardCharsets.UTF_8)
                .toString();

        String hashedPass = Hashing.sha256().hashString(password, StandardCharsets.UTF_8).toString();

        if (loginService.registerUser(hashedUser, hashedPass)) {
            return ResponseEntity.ok().body("Registration successful");
        }
        return ResponseEntity.status(401).body("Registration unsuccessful");
    }

    @GetMapping("/gh-oauth")
    public ResponseEntity<?> githubOAuth(@RequestParam("code") String code) {
        // String accessToken = loginService.fetchAccessToken(code);
        // if (accessToken == null) {
        //     return ResponseEntity.badRequest().body("Failed to retrieve access token");
        // }

        // System.out.println(accessToken);

        // Map<String, Object> userInfo = loginService.fetchGitHubUserInfo(accessToken);
        // if (userInfo == null) {
        //     return ResponseEntity.badRequest().body("Failed to retrieve user info");
        // }

        // System.out.println(userInfo);

        // String userLogin = (String) userInfo.get("login");
        // return ResponseEntity.ok().body("GitHub User Login: " + userLogin);

        // // Authenticate against database records
        // UserDetails userDetails = userDetailsService.loadUserByUsername(userLogin);
        // if (userDetails == null) {
        //     return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("User does not exist");
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
            return ResponseEntity.badRequest().body("Login unsuccessful");
        }

        String username = loginRequest.getUsername();
        String password = loginRequest.getPassword();

        String hashedUser = Hashing.sha256()
                .hashString(username, StandardCharsets.UTF_8)
                .toString();

        String hashedPass = Hashing.sha256().hashString(password, StandardCharsets.UTF_8).toString();

        if (loginService.fetchLoginData(hashedUser, hashedPass)) {
            String sessionToken = loginService.logSessionToken(hashedUser);
            return ResponseEntity.ok().body("Successful Login.\nSession Token: " + sessionToken);
        }
        return ResponseEntity.status(401).body("Login unsuccessful");
    }
}
