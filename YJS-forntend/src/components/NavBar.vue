<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- Hamburger Icon -->
      <div class="hamburger" @click="toggleMenu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
      <!-- Logo -->
      <div class="logo">
        <img src="@/assets/profile.png" alt="Logo" class="logo-img" />
      </div>
    </div>
  </nav>
</template>

<script>
  export default {
    data() {
      return {
        menuActive: true,
      };
    },
    methods: {
      toggleMenu() {
        this.menuActive = !this.menuActive;
      },
    },
  };
</script>
<style scoped>
  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #fcfcfc;
    color: #fff;
    z-index: 5;
    height: 64px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 90%;
    max-width: 1200px;
  }

  .logo {
    display: flex;
    align-items: center;
  }

  .logo img {
    width: 36px;
    height: 36px;
    margin-right: 10px;
    opacity: 1;
  }
  .hamburger {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    background-color: blue;
    width: 100px;
    height: 50px;
  }
  .bar {
    width: 50px;
    height: 5px;
    background-color: rgb(252, 146, 9);
  }
</style>
