<script>
import defaultPrinterImage from '@/assets/printer.png';

export default {
    props: {
        printer_status: {
            type: String,
            default: "Offline"
        },
        printer_image: {
            type: String,
            default: defaultPrinterImage
        },
        printer_title: {
            type: String,
            default: "Unknown Printer"
        },
        printer_type: {
            type: String,
            default: "Unknown Type"
        }
    },
    mounted() {
        // Set imageUrl based on the printer_image prop
        this.imageUrl = this.printer_image;
    },
    data() {
        return {
            imageUrl: ''
        };
    },
}
</script>

<template>
    <PrimeCard class="printer-card-style">
        <template #content>
            <div class="h-container">
                <div class="card-printer-image-container">
                    <!-- Use imageUrl for the image source -->
                    <img class="card-printer-image" :src="imageUrl" alt="printer-image">
                </div>
                <div>
                    <h3 class="printer-card-header">
                        {{ printer_type }}
                    </h3>
                    <p class="printer-card-data">
                        {{ printer_title }}
                    </p>
                    <p class="printer-card-sub">
                        {{ printer_status }}
                    </p>
                </div>
            </div>
        </template>
    </PrimeCard>
</template>

<style>
.card-printer-image-container{
    width: 100%;
    margin: 1rem;
}
.card-printer-image{
    width: 50%;
    margin: 0px;
}


.printer-card-style{
    width: 100%;
    min-width: 200px;
    margin-top: 20px;
    margin-bottom: 20px;
    background-color: #ffffff;
    border-radius: 5px;
    color: #000000;
    box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -webkit-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -moz-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
}

.printer-card-style:hover{
    background-color: #e9e9e9;
}


.printer-card-header{
    margin: 0.2rem;
    font-size: 1.1rem;
    font-weight: 300;
    font-family: 'FormaDJRMicro';
}

.printer-card-data{
    margin: 0.2rem;
    font-size: 1.5rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.printer-card-sub{
    margin: 0.2rem;
    font-size: 0.9rem;
    font-weight: 300;
    font-family: 'FormaDJRMicro';
}

</style>