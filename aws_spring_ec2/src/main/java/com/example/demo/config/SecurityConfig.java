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
        http.csrf(csrf -> csrf.ignoringRequestMatchers("/login", "/registration")) // double check if
                .authorizeHttpRequests((authorize) -> authorize
                        .requestMatchers("/login").permitAll() // unauthenticated users can acccess login page
                        .requestMatchers("/printers/**").authenticated() // unauthenticated users cannot access
                                                                         // endpoints that include "printers"
                        .anyRequest().permitAll())
                .requiresChannel(channel -> channel.anyRequest().requiresSecure()); // for enabling https
        return http.build(); // required
    }
}
