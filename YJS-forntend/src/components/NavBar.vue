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
        <p>幹部 FT-C1033</p>
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
    color: #000000;
    z-index: 20;
    height: 64px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
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
    background-color: rgb(255, 255, 255);
    width: 28px;
    height: 28px;
  }
  .bar {
    width: 2rem;
    height: 0.25rem;
    background-color: rgb(0, 0, 0);
    border-radius: 5px;
  }
</style>
