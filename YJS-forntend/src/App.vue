<template>
  <div id="app">
    <nav-bar />
    <side-bar />
    <div class="main-content">
      <breadcrumbs />
      <router-view />
    </div>
  </div>
</template>

<script>
  export default {
    name: "App",
  };
</script>

<style scoped>
  #app {
    font-family: "Inter", sans-serif;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: baseline;
    width: 100%;
  }

  nav-bar {
    flex: 0 0 20%;
  }

  side-bar {
    flex: 0 0 25%;
  }

  .main-content {
    flex: 1;
  }
</style>
