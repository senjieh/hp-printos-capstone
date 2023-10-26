<script>
import { ref } from 'vue';
export default {
  setup() {
    const text = ref('');
    const dates = ref([]);  // Declare dates as an array
    return { text, dates }; // Return dates so it's available in the template
  },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March', 'April', 'May'],
        datasets: [
          {
            label: 'My First Dataset',
            data: [65, 59, 80, 81, 56],
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }
        ]
      }
    };
  }
};
</script>

<template>
  <div class="h-container">
    <span class="p-float-label">
      <InputText id="txt" type="text" v-model="text"/>
      <label for="txt">Printer ID</label>
    </span>


    <PrimeCalender v-model="dates" selectionMode="multiple" :manualInput="false" />
    <PrimeChart type="line" :data="chartData"></PrimeChart>
    <PrimeButton label="doesnothing">Get Data</PrimeButton>
  </div>
</template>

<style>
.v-container{
  display: flex;
  align-items: center;
  justify-content: center;

}
.h-container{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
