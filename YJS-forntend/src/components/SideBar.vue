<template>
  <nav class="sidebar fixed-top">
    <div class="sidebar-brand">
      <router-link :to="'/'" class="head">YJS </router-link>
      <router-link :to="'/'" class="content">employee training</router-link>
    </div>
    <ul class="sidebar-nav">
      <li class="nav-item" v-for="item in navItems" :key="item.name">
        <router-link :to="item.to" class="nav-link" active-class="active">
          {{ item.label }}
        </router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup>
  const navItems = [
    { name: "Home", to: "/", label: "首頁" },
    { name: "Permissions", to: "/permissions", label: "人員與權限管理" },
    {
      name: "TrainingContent",
      to: "/training-content",
      label: "教育訓練內容管理",
    },
    { name: "PlanningModule", to: "/planning-module", label: "規劃模組" },
    { name: "ExecutionModule", to: "/execution-module", label: "執行模組" },
    { name: "AuditModule", to: "/audit-module", label: "查核模組" },
    { name: "AnalysisModule", to: "/analysis-module", label: "分析模組" },
  ];
</script>

<style scoped>
  .sidebar {
    width: 228px;
    height: calc(100vh - 100px);
    gap: 0px;
    background-color: #f1f1f1;
    padding: 10px;
    display: flex;
    align-content: flex-start;
    flex-wrap: wrap;
    align-items: center;
    z-index: 5;
    margin-top: 64px;
    overflow-y: auto;
  }

  .sidebar.fixed-top {
    top: 0;
    left: 0;
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
    align-content: center;
    height: 47px;
  }

  .nav-item a {
    display: flex;
    color: #333;
    width: inherit;
    font-size: 24px;
    font-family: Inter;
    font-weight: 400;
    line-height: 29.05px;
    text-align: left;
    text-underline-position: from-font;
    text-decoration-skip-ink: none;
    justify-content: flex-start;
    align-items: center;
  }

  .nav-item:hover {
    background-color: #ddd;
  }

  /* 可以為 .nav-link 加上額外的樣式 */
  .nav-link {
    height: inherit;
    text-decoration: none;
    color: inherit;
  }

  .nav-link.active {
    background-color: #ddd;
  }
</style>
