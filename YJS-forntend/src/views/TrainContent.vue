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

    <div class="demo">
      <div></div>
      <p>/</p>
      <p>/</p>
      <p>/</p>

      <base-button buttonType="primary" :disabled="true" @click="toggleMenu"
        >評量考核內容準備</base-button
      >
      <base-button buttonType="new" :buttonBackground="true"
        >新增課程
      </base-button>
      <base-button buttonType="new" :buttonBackground="false"
        >新增課程</base-button
      >
      <base-button buttonType="delete" :buttonBackground="true"
        >刪除常見缺失</base-button
      >
      <base-button buttonType="delete" :buttonBackground="false"
        >刪除常見缺失</base-button
      >
      <base-button buttonType="modify">上傳/修改詳細資料</base-button>
      <base-button buttonType="edit">儲存</base-button>
    </div>
  </div>
  <router-view />
</template>

<script setup>
  import { ref, watch } from "vue";
  import { useRoute } from "vue-router"; // 引入 useRoute

  const menu = ref(true);
  const route = useRoute();

  const toggleMenu = () => {
    menu.value = !menu.value;
    console.log(menu.value);
  };

  watch(route, () => {
    if (route.name === "training-content") {
      menu.value = true; // 每次路由變化都顯示 menu
      console.log("Route changed, menu is reset", menu.value);
    }
  });
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
