package com.example.demo.model;

public class Printer {
        private long totalPrinted;
        private long totalDropped;
        private long totalPlanned;
        private long timestampStart;
        private long timestampEnd;
    
        // Constructor for ease of use
        public Printer() {
            this.totalPrinted = 0;
            this.totalDropped = 0;
            this.totalPlanned = 0;
            this.timestampStart = 0;
            this.timestampEnd = 0;
        }
    
        // Getters
        public long getTotalPrinted() {
            return totalPrinted;
        }
    
        public long getTotalDropped() {
            return totalDropped;
        }
    
        public long getTotalPlanned() {
            return totalPlanned;
        }

        public long getTimestampStart() {
            return timestampStart;
        }

        public long getTimestampEnd() {
            return timestampEnd;
        }
    
        // Setters
        public void setTotalPrinted(long totalPrinted) {
            this.totalPrinted = totalPrinted;
        }
    
        public void setTotalDropped(long totalDropped) {
            this.totalDropped = totalDropped;
        }
    
        public void setTotalPlanned(long totalPlanned) {
            this.totalPlanned = totalPlanned;
        }

        public void setTimestampStart(long timestampStart) {
            this.timestampStart = timestampStart;
        }
        public void setTimestampEnd(long timestampEnd) {
            this.timestampEnd = timestampEnd;
        }
    
        @Override
        public String toString() {
            return "PrinterMetrics{" +
                   "totalPrinted=" + totalPrinted +
                   ", totalDropped=" + totalDropped +
                   ", totalPlanned=" + totalPlanned +
                   ", timestampStart=" + timestampStart +
                   ", timestampEnd=" + timestampEnd +
                   '}';
        }
    }