package com.example.demo.model;

public class Printer {
    private int id;
    private String type;
    private String model;
    private int last_update;
    private int user;
    private int connection_start; // if we wanted to not have this field appear in json, use some annotation
                                  // @jsonignore
    private String printer_image;

    // Constructor for ease of use
    public Printer() {
        this.id = 0;
        this.type = "";
        this.model = "";
        this.printer_image = "";
        this.connection_start = 0;
        this.last_update = 0;
        this.user = 0;
    }

    // Getters
    public int getID() {
        return id;
    }

    public String getType() {
        return type;
    }

    public String getModel() {
        return model;
    }

    public int getConnectionStart() {
        return connection_start;
    }

    public String getPrinterImage() {
        return printer_image;
    }

    public int getLastUpdate() {
        return last_update;
    }

    public int getUser() {
        return user;
    }

    // Setters
    public void setID(int printer_id) {
        this.id = printer_id;
    }

    public void setUserID(int user_id) {
        this.user = user_id;
    }

    public void setType(String printer_type) {
        this.type = printer_type;
    }

    public void setModel(String printer_model) {
        this.model = printer_model;
    }

    public void setLastUpdate(int last_printer_connection) {
        this.last_update = last_printer_connection;
    }

    public void setConnectionStart(int connection_start_value) {
        this.connection_start = connection_start_value;
    }

    public void setPrinterImage(String printer_image_link) {
        this.printer_image = printer_image_link;
    }

    @Override
    public String toString() {
        return "PrinterMetrics{" +
                "id =" + id +
                ", type=" + type +
                ", model=" + model +
                ", last_update=" + last_update +
                ", printer_image=" + printer_image +
                ", connection_start=" + connection_start +
                '}';
    }
}