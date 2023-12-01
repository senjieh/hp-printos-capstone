<script>
import hplogo from '@/assets/hplogo.png';
import homepageicon from '@/assets/homepageicon.png';
import printericon from '@/assets/printericon.png';
// import darkmodeicon from @/assets/
import { state } from '@/store/store.js'; 

export default {
  props: {
    dark_mode_setting: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      logoImagePath: hplogo,
      homepageImagePath: homepageicon,
      printerImagePath: printericon
      // darkModeImagePath: darkmodeicon
    }
  },
  methods: {
    goToHomePage() {
      this.$router.push('/');
    },
    goToPrinterPage() {
      this.$router.push('/printers');
    }
  },
  setup() {
    const toggleDarkMode = () => {
      state.isDarkMode = !state.isDarkMode; // Toggle dark mode in global state
    };
    return { state, toggleDarkMode };
  }

}
</script>
<template>
  <div class="nav-bar-div" :class="{ 'dark-mode': dark_mode_setting }">
    <img class="nav-bar-logo" :src="logoImagePath" alt="hp-logo">
    <button class="nav-button" @click="goToHomePage">
        <img class="nav-bar-icon" :src="homepageImagePath" alt="homepage-icon">
    </button>
    <button class="nav-button" @click="goToPrinterPage">
        <img class="nav-bar-icon" :src="printerImagePath" alt="printer-icon">
    </button>
    <InputSwitch class="darkmode-switch" v-model="isDarkMode" @change="toggleDarkMode">
    </InputSwitch>
  </div>
</template>


<style>

.nav-bar-div{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 90px;
    margin-right: 100px;
    height: 100vh;
    background-color: white;
    z-index: 1;
    box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -webkit-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
    -moz-box-shadow: -2px 2px 20px 5px rgba(0,0,0,0.05);
}

.nav-bar-div.dark-mode{
    background-color: #000000;
    box-shadow: -2px 2px 20px 5px rgba(255, 255, 255, 0.05);
    -webkit-box-shadow: -2px 2px 20px 5px rgba(255, 255, 255, 0.05);
    -moz-box-shadow: -2px 2px 20px 5px rgba(255, 255, 255, 0.05);
}

.nav-bar-logo{
    width: 45px;
    margin-top: 20px;
    margin-bottom: 20px;
}
.nav-bar-icon{
    width: 23px;
    opacity: 75%;
}
.nav-button{
    margin-top: 20px;
    color: white;
    border-radius: 30px;
    opacity: 50%;
    width: fit-content;
    padding: 15px;
    border: none;
    background-color: white;
}
.nav-button:hover{
    opacity: 100%;
    margin-top: 20px;
    color: white;
    border-radius: 30px;
    width: fit-content;
    padding: 15px;
    border: none;
    background-color: #f0f0f0;
}

/* Dark mode specific styles */
.nav-bar-div.dark-mode {
  background-color: #060606; /* Dark background */
  /* Add any other style changes needed for dark mode here */
}

.nav-bar-div.dark-mode .nav-button {
  color: #fff; /* Light text for dark background */
  background-color: #333; /* Dark button background */
}

.nav-bar-div.dark-mode .nav-button:hover {
  background-color: #444; /* Slightly lighter background on hover */
}

.darkmode-switch {
  margin-top: 20px;  
}
</style>