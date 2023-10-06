<template>
  <div>
    <button @click="showMessage = true">Click me</button>
    <p v-if="showMessage">Hello World</p>
    <button @click="fetchData">Get data</button>
    <ul v-if="apiData">
        <li v-for="fact in apiData" :key="fact._id">{{ fact.text }}</li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() { //keeps track of local data of HelloWorld component
    return {
      showMessage: false,
      apiData: null
    }
  },
  methods: {
    fetchData() {
      axios.get('https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=2')
      .then(response => {
        this.apiData = response.data;
      })
      .catch(error => {
        console.error('Error fetching data: ', error);
      });
    }
  },
  created() { //keeps track of any 
    
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
