<template>
  <!-- <side-bar></side-bar> -->
  <div class="main-container">
    <nav-bar></nav-bar>
    <side-bar></side-bar>
    <content-manager></content-manager>
  </div>
</template>

<script></script>

<style scoped>
  .main-container {
    font-family: "Inter", sans-serif;
    display: flex;
    flex-wrap: wrap; /* 避免換行 */
    justify-content: space-between; /* 使子元素間有適當間距 */
    align-items: flex-start;
    width: 100%; /* 讓容器佔據全寬 */
  }

  nav-bar {
    flex: 0 0 20%; /* nav-bar佔據20%的寬度 */
  }

  side-bar {
    flex: 0 0 25%; /* side-bar佔據25%的寬度 */
  }

  content-manager {
    flex: 1; /* content-manager佔據剩餘的空間 */
  }
</style>
