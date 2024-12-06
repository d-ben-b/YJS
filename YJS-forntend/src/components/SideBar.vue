<template>
  <nav class="navbar fixed-top">
    <div class="navbar-brand">
      <a href="#">YJS employee training</a>
    </div>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a href="#">首頁</a>
      </li>
      <li class="nav-item">
        <a href="#">人員與權限管理</a>
      </li>
      <li class="nav-item">
        <a href="#">教育訓練內容管理</a>
      </li>
      <li class="nav-item">
        <a href="#">規劃模組</a>
      </li>
      <li class="nav-item">
        <a href="#">執行模組</a>
      </li>
      <li class="nav-item">
        <a href="#">查核模組</a>
      </li>
      <li class="nav-item">
        <a href="#">分析模組</a>
      </li>
    </ul>
  </nav>
</template>

<script>
  export default {
    name: "SideBar",
  };
</script>

<style>
  .navbar {
    background-color: #f1f1f1;
    padding: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 1000; /* 確保導航欄在頁面上方 */
  }

  .navbar.fixed-top {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
  }

  .navbar-brand a {
    font-size: 20px;
    font-weight: bold;
    text-decoration: none;
    color: #333;
  }

  .navbar-nav {
    list-style-type: none;
    display: flex;
    margin: 0;
    padding: 0;
  }

  .nav-item a {
    text-decoration: none;
    color: #333;
    padding: 10px;
    margin: 0 5px;
  }

  .nav-item a:hover {
    background-color: #ddd;
  }
</style>
