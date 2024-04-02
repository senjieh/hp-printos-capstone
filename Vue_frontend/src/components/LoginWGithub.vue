<script>
export default {
  name: 'LoginWGithub',
  methods: {
    loginWithGitHub() {
      const clientId = '779416e0c602f567e686';
      const redirectUri = 'http://localhost:8080/gh-oauth';
      const scope = 'user:email,read:user';
      const authorizationUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}`;
      window.location.href = authorizationUrl;
    }
  }
}
</script>

<template>
  <div>
    <button @click="loginWithGitHub">Login with GitHub</button>
  </div>
</template>

<style scoped>
/* Your component's styles go here */
</style>