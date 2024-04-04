<script>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRoute } from 'vue-router'; // Import useRoute to access router parameters
import axios from 'axios';
import defaultPrinterImage from '@/assets/printer.png';
import { state } from '@/store/store.js';
import { format } from 'date-fns';

export default { 
    props: {
        dark_mode_setting: {
            type: Boolean,
            default: false
        }
    },
    methods: {
        goToPage() {
            this.$router.push({ path: '/printers' });
        }
    },
    setup() {
        const formattedTimeElapsed = ref('');
        const KPIData = ref([]);
        const dates = ref([]);
        const printerDetails = ref([]);
        const printerStatus = ref('');
        const imageUrl = ref(defaultPrinterImage)
        const intervalId = ref(null);

        const route = useRoute();
        const printer_id_param = computed(() => route.params.id);

        const chartData = ref({
            labels: [],
            datasets: [{
                label: '',
                data: [],
                fill: false,
                tension: 0.5,
                borderColor: '#0067ff',
                pointRadius: 4,
                pointBackgroundColor: '#0067ff',
            }]
        });

        // Convert timestamp to ISO format
        const convertTimestampToISO = (timestamp) => new Date(timestamp * 1000).toISOString();

        // Convert timestamp to month day format
        const convertTimestampToMonthDay = (timestamp) => {
            const date = new Date(timestamp * 1000);
            const monthDay = format(date, 'M/d');
            return monthDay;
        }

        const fetchData = async (printer_id) => {
            console.log(printer_id);
            try {
                const startTimestamp = parseInt(dates.value[0].getTime() / 1000, 10);
                const endTimestamp = parseInt(dates.value[1].getTime() / 1000, 10);
                console.log(startTimestamp);
                console.log(endTimestamp);
                const graph_url = `https://indacloudtoo.com/printers/${printer_id}/print-data?date_start=${startTimestamp}&date_end=${endTimestamp}&interval=hour`;
                const printer_data_url = `https://indacloudtoo.com/printers/${printer_id}/print-data?date_start=${startTimestamp}&date_end=${endTimestamp}&interval=month`;
                const printer_details_url = `https://indacloudtoo.com/printers/${printer_id}/printer-details`;

                console.log(printer_data_url);
                const graph_url_response = await axios.get(graph_url);
                console.log(graph_url_response.data);

                // populating graph
                if (graph_url_response.data.length === 0) {
                    chartData.value.labels = [];
                    chartData.value.datasets[0].data = []; // double check if empty array is valid
                } else {
                    chartData.value.labels = graph_url_response.data.map(item => convertTimestampToMonthDay(item.timestampStart));
                    console.log(chartData.value.labels);
                    chartData.value.datasets[0].data = graph_url_response.data.map(item => item.totalPrinted);
                }
                
                // populating aggregate cards
                const printer_data_url_response = await axios.get(printer_data_url);
                console.log(printer_data_url_response.data);
                if (printer_data_url_response.data.length === 0) {
                    KPIData.value.totalPrinted = 0;
                    KPIData.value.totalDropped = 0;
                    KPIData.value.totalPlanned = 0;
                } else {
                    KPIData.value = printer_data_url_response.data[0];
                }
                
                const printer_details_url_response = await axios.get(printer_details_url);
                printerDetails.value = printer_details_url_response.data;
                
                console.log(printer_details_url_response.data);
                imageUrl.value = printer_details_url_response.data[0].printerImage;

            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };
        
        const printerStatusCalc = (lastUpdateTimestamp) => {
        
            const now = new Date();
            const fiveMinutes = 300000; 
            const lastUpdateTime = new Date(lastUpdateTimestamp);

            const status = () => (now - lastUpdateTime <= fiveMinutes? 'Online' : 'Offline');

            printerStatus.value = status();
        };

        const formatTime = (seconds) => {
            const pad = (num) => (num < 10 ? '0' + num : num);

            let hours = Math.floor(seconds / 3600);
            let minutes = Math.floor((seconds % 3600) / 60);
            let secondsLeft = seconds % 60;

            return `${pad(hours)}:${pad(minutes)}:${pad(secondsLeft)}`;
        };

        const updateTimeElapsed = () => {
            if (!printerDetails.value[0].connectionStart) {
                formattedTimeElapsed.value = '00:00:00';
                return;
            }

            const currentTime = Math.floor(Date.now() / 1000);

            const timeElapsedInSeconds = currentTime - printerDetails.value[0].connectionStart;
            formattedTimeElapsed.value = formatTime(timeElapsedInSeconds);
        };

        onMounted(() => {
            /* This is where the date range is auto-populated */
            const today = new Date();
            const oneMonthAgo = new Date(new Date().setMonth(today.getMonth() - 1));

            dates.value = [oneMonthAgo, today];
            fetchData(printer_id_param.value);
            printerStatusCalc();
            intervalId.value = (printerStatus.value == "Online" ? setInterval(updateTimeElapsed, 1000) : formattedTimeElapsed.value = "N/A" );
        });

        onUnmounted(() => {
            clearInterval(intervalId.value);
        });

        return { state, dates, imageUrl, printerDetails, printerStatus, KPIData, chartData, formattedTimeElapsed, fetchData };
    }
}
</script>

<template>
    <div :class="{ 'dark-mode': state.isDarkMode }" class="hp-printer-page">
        <div class="print-div">
            <button class="blue-button" @click="goToPage">Printers</button>
            <h2 class="printer-type">{{ printerDetails.type }}</h2>
            <h2 class="printer-title">{{ printerDetails.model }}</h2>
            <img class="printer-image" :src="imageUrl" alt="printer-image">
            <div class="printer-stat-div">
                <div class="printer-stat-row">
                    <div class="printer-stat">
                        <p class="printer-stat-text">Printer Status</p>
                    </div>
                    <div class="printer-stat">
                        <p class="printer-stat-text"> {{ printerStatus }} </p>
                    </div>
                </div>
                <div class="printer-stat-row">
                    <div class="printer-stat">
                        <p class="printer-stat-text">Uptime</p>
                    </div>
                    <div class="printer-stat">
                        <p class="printer-stat-text"> {{ formattedTimeElapsed }} </p>
                    </div>
                </div>
                <div class="printer-stat-row">
                    <div class="printer-stat">
                        <p class="printer-stat-text">Uptime %</p>
                    </div>
                    <div class="printer-stat">
                        <p class="printer-stat-text">90%</p>
                    </div>
                </div>
                <div class="printer-stat-row">
                    <div class="printer-stat">
                        <p class="printer-stat-text">Toner Remaining</p>
                    </div>
                    <div class="printer-stat">
                        <p class="printer-stat-text">25%</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="stat-div">
            <div class="card-row">
                <PrimeCard :class="{ 'dark-mode': state.isDarkMode }" class="card-style" v-if="KPIData">
                    <template #content>
                        <h3 class="card-header">Total Pages</h3>
                        <p class="card-data">
                            {{ KPIData.totalPlanned }} Pages  
                        </p>
                        <p class="card-sub">
                            Up 52% from last month
                        </p>
                    </template>
                </PrimeCard>
                <PrimeCard :class="{ 'dark-mode': state.isDarkMode }" class="card-style" v-if="KPIData">
                    <template #content>
                        <h3 class="card-header">Pages Dropped</h3>
                        <p class="card-data">
                            {{ KPIData.totalDropped }} Pages  
                        </p>
                        <p class="card-sub">
                            Up 52% from last month
                        </p>
                    </template>
                </PrimeCard>
                <PrimeCard :class="{ 'dark-mode': state.isDarkMode }" class="card-style" v-if="KPIData">
                    <template #content>
                        <h3 class="card-header">Pages Printed</h3>
                        <p class="card-data">
                            {{ KPIData.totalPrinted }} Pages  
                        </p>
                        <p class="card-sub">
                            Up 52% from last month
                        </p>
                    </template>
                </PrimeCard>

            </div>
            <PrimeCard :class="{ 'dark-mode': state.isDarkMode }" class="card-style">
                    <template #content>
                        <PrimeCalendar v-model="dates" selectionMode="range" :manualInput="false" />
                        <PrimeChart type="line" :data="chartData"></PrimeChart>
                    </template>
            </PrimeCard>
        </div>


    </div>
</template>


<style>


.printer-stat-div{
    width: 100%;
    display: flex;
    flex-direction: column;
}

.printer-stat-row{
    display: flex;
    flex-direction: row;
    margin: 0.5rem;
    margin-right: 5rem;
    justify-content: space-between;
}

.printer-stat-text{
    font-size: 1rem;
    font-weight: 300;
}

.hp-printer-page{
    display: flex;
    flex-direction: row;
    color:#2e2e2e;
    background-color: #f9f9f9;
    width: 95%;
    max-height: 100vh;
    overflow: scroll;
}

.hp-printer-page.dark-mode{
    background-color: #060606;
    color: #ffffff;
}

.card-row{
    display: flex;
    flex-direction: row;
}

.print-div{
    display: flex;
    flex-direction: column;
    width: 30%;
    margin-right: 7%;
    padding: 1rem;
}

.printer-title{
    margin: 0px;
    margin-bottom: 2.4rem;
    font-size: 3rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.printer-image {
    height: auto;
    margin-top: 1rem;
    margin-bottom: 2rem;
    width: 90%;
    max-height: 50vh; /* or 50% depending on the container */
    object-fit: contain;
    object-position: left; /* Adjusts the position of the image within its frame */
}

.printer-type{
    color: #afafaf;
    margin-bottom: 0.5rem;
    font-size: 2.3rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.stat-div{
    width: 60%;
}

.card-style{
    border-radius: 15px;
    width: 98%;
    background-color: #ffffff;
    color: #2e2e2e;
    margin: 1%;
    padding: 0.5rem;
    box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -webkit-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -moz-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
}

.card-style.dark-mode {
    background-color:#323232;
    color: #ffffff;
}

.card-header{
    margin: 0.2rem;
    font-size: 1.1rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.card-data{
    margin: 0.2rem;
    font-size: 2.2rem;
    font-weight: 500;
    font-family: 'FormaDJRMicro';
}

.card-sub{
    margin: 0.2rem;
    font-size: 0.9rem;
    font-weight: 300;
    font-family: 'FormaDJRMicro';
}
</style>