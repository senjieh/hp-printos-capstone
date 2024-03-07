package com.example.demo;

import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Assertions.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.web.servlet.MockMvc;
import org.junit.jupiter.api.Test;
import static org.mockito.BDDMockito.*;

import com.example.demo.device_provisioning_api.controller.DeviceProvisioningController;
import com.example.demo.device_provisioning_api.model.Device;
import com.example.demo.device_provisioning_api.service.DeviceProvisioningService;

@WebMvcTest(DeviceProvisioningController.class)
public class DeviceProvisioningTests {

    // @Test
    // // this one is supposed to be a unit test but it feels like I am testing both
    // // the service, model, and controller
    // void testController() {
    // DeviceProvisioningController controller = new DeviceProvisioningController();
    // Device device = new Device();

    // final MockMvc mvc;
    // final DeviceProvisioningService service;

    // given(service.registerDevice()).willReturn(true);

    // // use mockito to
    // mvc.perform(post("/devices/registration"))
    // .andExpect(status().isOk());
    // }

}
