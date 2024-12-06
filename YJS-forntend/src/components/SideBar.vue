<template>
  <nav class="sidebar fixed-top">
    <div class="sidebar-brand">
      <router-link to="/" class="head">YJS </router-link>
      <router-link to="/" class="content">employee training</router-link>
    </div>
    <ul class="sidebar-nav">
      <li class="nav-item">
        <router-link to="/" class="nav-link">首頁</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/permissions" class="nav-link"
          >人員與權限管理</router-link
        >
      </li>
      <li class="nav-item">
        <router-link to="/training-content" class="nav-link"
          >教育訓練內容管理</router-link
        >
      </li>
      <li class="nav-item">
        <router-link to="/planning-module" class="nav-link"
          >規劃模組</router-link
        >
      </li>
      <li class="nav-item">
        <router-link to="/execution-module" class="nav-link"
          >執行模組</router-link
        >
      </li>
      <li class="nav-item">
        <router-link to="/audit-module" class="nav-link">查核模組</router-link>
      </li>
      <li class="nav-item">
        <router-link to="/analysis-module" class="nav-link"
          >分析模組</router-link
        >
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
    margin-top: 20px;
    padding: 0;
    width: inherit;
  }

  .nav-item {
    height: 47px;
  }

  .nav-item a {
    color: #333;
    padding: 10px;
    margin: 5px 5px;
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

  /* 可以為 .nav-link 加上額外的樣式 */
  .nav-link {
    text-decoration: none;
    color: inherit;
  }

  .nav-link.active {
    background-color: #ddd;
  }
</style>
