<template>
  <div id="app">
    <NavBar />
    <SideBar />
    <router-view />
  </div>
</template>

<script>
  import NavBar from "@/components/NavBar.vue";
  import SideBar from "./components/SideBar.vue";

  export default {
    name: "App",
    components: {
      NavBar,
      SideBar,
    },
  };
</script>

<style scoped>
  #app {
    font-family: "Inter", sans-serif;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
  }

  nav-bar {
    flex: 0 0 20%;
  }

  side-bar {
    flex: 0 0 25%;
  }

  content-manager {
    flex: 1;
  }
</style>
