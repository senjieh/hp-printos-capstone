package com.example.demo.model;

public class Printer {
        private Long id;
        private Long job_id;       // Added this field
        private int pages;         // Added this field
        private int pages_printed; // Added this field
        private int pages_dropped; // Added this field
        private String timestamp;  // Added this field

        // Default constructor
        public Printer() {
        }

        // Parameterized constructor
        public Printer(Long id, String brand,
                       Long job_id, int pages, int pages_printed, int pages_dropped, String timestamp) {
            this.id = id;
            this.job_id = job_id;
            this.pages = pages;
            this.pages_printed = pages_printed;
            this.pages_dropped = pages_dropped;
            this.timestamp = timestamp;
        }
    // Getter and Setter methods

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }


    public Long getJobId() {
        return job_id;
    }

    public void setJobId(Long job_id) {
        this.job_id = job_id;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    public int getPagesPrinted() {
        return pages_printed;
    }

    public void setPagesPrinted(int pages_printed) {
        this.pages_printed = pages_printed;
    }

    public int getPagesDropped() {
        return pages_dropped;
    }

    public void setPagesDropped(int pages_dropped) {
        this.pages_dropped = pages_dropped;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }
}
