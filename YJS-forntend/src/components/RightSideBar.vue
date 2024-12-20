<template>
  <div class="overlay" v-if="show">
    <div class="sidebar">
      <div v-if="loading">載入中...</div>
      <div v-else>
        <base-button buttonType="edit" :buttonBackground="true"
          >編輯</base-button
        >
        <button class="close-btn" @click="show = !show">✖</button>
        <ul>
          <MenuItem v-for="menu in menus" :key="menu.id" :item="menu" />
        </ul>
      </div>
      <div v-if="error" class="error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import MenuItem from "./MenuItem.vue";

  const menus = ref([]);
  const loading = ref(true);
  const error = ref(null);
  const show = ref(true);

  const fetchMenus = async () => {
    try {
      const response = await axios.get("/api/menus"); // 更新為您的 API URL
      menus.value = response.data.map((dept) => ({
        ...dept,
        open: false,
        children: dept.children.map((unit) => ({
          ...unit,
          open: false,
          children: unit.children.map((ws) => ({
            ...ws,
            open: false,
            children: ws.children.map((wi) => ({
              ...wi,
              open: false,
              children: [], // 最下層不再有子項目
            })),
          })),
        })),
      }));
    } catch (err) {
      console.error("取得選單資料失敗:", err);
      error.value = "無法取得選單資料。請稍後再試。";
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    fetchMenus();
  });
</script>

<style scoped>
  .sidebar {
    width: 280px;
    background-color: #ffffff;
    padding: 20px;
    border-left: 1px solid #d9d9d9;
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    overflow-y: auto;
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
  }

  .overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1000;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    position: absolute;
    top: 15px;
    right: 20px;
    color: #333;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;
    font-family: Arial, sans-serif;
    font-size: 14px;
  }

  ul > li {
    padding: 10px 0;
    border-bottom: 1px solid #eaeaea;
  }

  .menu-item {
    font-weight: bold;
    cursor: pointer;
    padding: 8px 0;
  }

  .menu-item:hover {
    color: #007bff;
  }

  ul ul {
    padding-left: 15px;
    margin: 10px 0;
    border-left: 2px solid #d9d9d9;
  }

  ul ul li {
    padding: 5px 0;
  }

  ul ul li:hover {
    color: #007bff;
  }

  .error {
    color: #d9534f;
    margin-top: 10px;
    font-size: 14px;
    text-align: center;
  }

  .sidebar h3 {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 15px;
    color: #333;
  }
</style>
