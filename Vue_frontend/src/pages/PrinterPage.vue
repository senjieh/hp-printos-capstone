<script>
import PrinterCard from '@/components/PrinterCard.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { state } from '@/store/store.js'; 

export default {
    props: {
        dark_mode_setting: {
            type: Boolean,
            default: false
        }
    },
    components: {
        PrinterCard,
    },
    setup() {
        const printers = ref([]);

        const fetchData = async () => {
            try {
                const url = `https://indacloudtoo.com/user/printers?user_id=1`;
                const response = await axios.get(url);
                printers.value = response.data;

                console.log(response.data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        }

        onMounted(fetchData);

        return { printers, state };
    }
}
</script>

<template>
    <div :class="{ 'dark-mode': dark_mode_setting }" class="printer-view-container" >
        <div>
            <h2 class="printer-view-title">Printers</h2>
        </div>
        <div class="printer-card-container">
            <router-link
                v-for="(printer, index) in printers" 
                :key="index"
                :to="`/printers/${printer.id}`"
                custom
                v-slot="{ navigate }">
                <div class="printer-card-link" @click="navigate">
                    <PrinterCard
                        :dark_mode_setting = state.isDarkMode
                        :printer_status="printer.status" 
                        :printer_title="printer.model" 
                        :printer_image="printer.printerImage" 
                        :printer_type="printer.type">
                    </PrinterCard>
                </div>
            </router-link>
        </div>
    </div>
</template>



<style>
.printer-card-link {
    text-decoration: none;
    color: inherit;
    width: 25%;
    margin-right: 50px;
}

.printer-view-title{
    font-size: 2rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.printer-view-container{
    color: #000000;
    overflow: scroll;
    padding: 1rem;
    max-height: 100vh;
    width: 95%;
    height: 100vh;
}

.printer-card-container{
    display: flex;
    flex-direction: row;
    width: 100%
}

.printer-view-container.dark-mode{
    color: #ffffff;
    background-color: #060606;
}



</style>