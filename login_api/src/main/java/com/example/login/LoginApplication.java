package com.example.login;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.security.servlet.SecurityAutoConfiguration;

@SpringBootApplication(exclude = { SecurityAutoConfiguration.class }) // way to disable spring security for now
/*
 * Spring security requires configuration for which endpoints are pingable or
 * not.
 * Disabling it for now, so that we at least know that we can communicate
 * between database and frontend
 */
public class LoginApplication {

	public static void main(String[] args) {
		SpringApplication.run(LoginApplication.class, args);
	}

}
