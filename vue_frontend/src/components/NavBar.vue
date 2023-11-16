<script>
import hplogo from '@/assets/hplogo.png';
import homepageicon from '@/assets/homepageicon.png';
import printericon from '@/assets/printericon.png';
export default {
  data() {
    return {
      logoImagePath: hplogo,
      homepageImagePath: homepageicon,
      printerImagePath: printericon
    }
  },
  methods: {
    goToHomePage() {
      this.$router.push('/');
    },
    goToPrinterPage() {
      this.$router.push('/printers');
    }
  }

}
</script>
<template>
  <div class="nav-bar-div">
    <img class="nav-bar-logo" :src="logoImagePath" alt="hp-logo">
    <button class="nav-button" @click="goToHomePage">
        <img class="nav-bar-icon" :src="homepageImagePath" alt="homepage-icon">
    </button>
    <button class="nav-button" @click="goToPrinterPage">
        <img class="nav-bar-icon" :src="printerImagePath" alt="printer-icon">
    </button>
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


</style>