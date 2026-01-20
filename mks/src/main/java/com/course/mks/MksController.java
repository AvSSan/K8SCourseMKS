package com.course.mks;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.net.InetAddress;
import java.net.UnknownHostException;

@RestController
public class MksController {

    @GetMapping("/")
    public String index() {
        String hostName = "Unknown";
        try {
            hostName = InetAddress.getLocalHost().getHostName();
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }

        return "Привет! Это Java сервис MKS. Я работаю внутри контейнера: " + hostName;
    }

    @GetMapping("/status")
    public String status() {
        return "{\"status\": \"OK\", \"language\": \"Java 17\", \"framework\": \"Spring Boot\"}";
    }
}