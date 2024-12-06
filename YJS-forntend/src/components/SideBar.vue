<template>
  <nav class="sidebar fixed-top">
    <div class="sidebar-brand">
      <a href="#" class="head">YJS </a>
      <a href="#" class="content">employee training</a>
    </div>
    <ul class="sidebar-nav">
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

<style scoped>
  .sidebar {
    width: 248px;
    height: 770px;
    gap: 0px;
    background-color: #f1f1f1;
    padding: 10px;
    display: flex;
    align-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
    z-index: 5;
    margin-top: 64px;
  }

  .sidebar.fixed-top {
    top: 0;
    left: 0;
    right: 0;
  }

  .sidebar-brand .head {
    font-size: 28px;
    font-weight: 700;
    line-height: 33.89px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    color: #b82121;
    text-decoration: none;
  }

  .sidebar-brand .content {
    font-size: 16px;
    font-weight: 700;
    line-height: 19.36px;
    text-align: center;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    color: #b82121;
    text-decoration: none;
  }

  .sidebar-nav {
    list-style-type: none;
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    margin-top: 20px;
    padding: 0;
    width: inherit;
  }

  .nav-item a {
    color: #333;
    padding: 10px;
    margin: 0 5px;
    width: inherit;
    font-size: 24px;
    font-family: Inter;
    font-weight: 400;
    line-height: 29.05px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
  }

  .nav-item:hover {
    background-color: #ddd;
  }
</style>
