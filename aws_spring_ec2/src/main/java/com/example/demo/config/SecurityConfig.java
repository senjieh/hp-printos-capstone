package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http.csrf().disable() // Disable CSRF protection for simplicity
            .authorizeHttpRequests(authorize -> authorize
                .requestMatchers("/login", "/registration", "/gh-oauth").permitAll() // Allow access to login and registration endpoints
                .requestMatchers("/printers/**").authenticated() // Require authentication for /printers/** endpoints
                .anyRequest().permitAll() // Allow access to all other endpoints
            );
        return http.build();
    }
}