<template>
  <div class="container" v-show="menu">
    <router-link :to="{ name: 'content' }"
      ><base-button buttonType="primary" @click="toggleMenu"
        >課程內容準備</base-button
      >
    </router-link>
    <router-link :to="{ name: 'quiz' }"
      ><base-button buttonType="primary" @click="toggleMenu"
        >隨堂測驗內容準備</base-button
      ></router-link
    >

    <router-link :to="{ name: 'assessment' }"
      ><base-button buttonType="primary" @click="toggleMenu"
        >評量考核內容準備</base-button
      ></router-link
    >
  </div>
  <router-view />
</template>

<script setup>
  import { ref, watch, onMounted } from "vue";
  import { useRoute } from "vue-router";

  const menu = ref(true); // 控制 menu 顯示與隱藏
  const route = useRoute();
  onMounted(() => {
    if (route.name === "training-content") {
      menu.value = true;
    } else {
      menu.value = false;
    }
  });
  // 根據當前路由的名稱來顯示/隱藏 menu
  watch(route, (newRoute) => {
    // 檢查是否是需要隱藏 menu 的路由
    if (newRoute.name === "training-content") {
      menu.value = true;
    } else {
      menu.value = false;
    }
  });

  // toggleMenu 的功能不變
  const toggleMenu = () => {
    menu.value = !menu.value;
    console.log(menu.value);
  };
</script>

<style>
  .container {
    width: 100%;
    margin: 70px 45px;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    flex-wrap: wrap;
  }
  .container a {
    margin-right: 22px;
  }
</style>
