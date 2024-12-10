<template>
  <div class="not-found">
    <h1>404 - 頁面不存在</h1>
    <p>您訪問的頁面不存在，請檢查您的網址是否正確。</p>
    <router-link to="/">返回首頁</router-link>
  </div>
</template>

<script>
  export default {
    name: "NotFoundComponent",
  };
</script>

<style scoped>
  .not-found {
    text-align: center;
    padding: 50px;
  }
  .not-found h1 {
    font-size: 2em;
    margin-bottom: 20px;
  }
  .not-found p {
    margin-bottom: 30px;
  }
</style>
