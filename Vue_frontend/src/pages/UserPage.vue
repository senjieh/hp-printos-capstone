<template>
  <button @click="onLogout" type="button">Logout</button>
</template>

<script>
// import axios from 'axios';

export default {
props: {
dark_mode_setting: {
  type: Boolean,
  default: false
}
},
data() {
return {
  username: '',
  password: '',
  errorMessage: ''
}
},
methods: {
setCookie(name, value, days) {
  let expires = "";
  if (days) {
    const date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
},

removeCookie(name) {
  this.setCookie(name, '', -1); // Set the cookie to expire yesterday
},

onLogout() {
  this.removeCookie('user-token'); // Remove the user-token cookie
  this.$router.push('/login'); // Redirect to login page or home page after logout
},

}
}
</script>

<style>
/* Style remains the same */
.login-container {
max-width: 300px;
margin: auto;
padding: 20px;
border: 1px solid #ccc; 
border-radius: 5px;
color: black;
}

.login-container.dark-mode {
color: white;
}

.form-group {
margin-bottom: 15px;
}

.form-group label {
display: block;
margin-bottom: 5px;
}

.form-group input {
width: 100%;
padding: 8px;
border: 1px solid #ccc;
border-radius: 4px;
}

.error-dropdown {
position: fixed;
top: 0;
left: 0;
right: 0;
background-color: #ff3333; /* Red background */
color: white;
text-align: center;
padding: 10px;
z-index: 100;
}
</style>
