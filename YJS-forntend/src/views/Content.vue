<template>
  <!-- 根據 routerName 顯示不同的按鈕組 -->
  <template v-if="routerName === 'content'">
    <div class="container">
      <base-button buttonType="primary" @click="navigateTo('course-table')"
        >課程維護</base-button
      >
    </div>
  </template>
  <template v-else-if="routerName === 'quiz'">
    <div class="container">
      <base-button buttonType="primary" @click="navigateTo('course-table-view')"
        >查看課程詳細資料</base-button
      >
      <base-button buttonType="primary" @click="navigateTo('quiz-design')"
        >評量考核題目設計</base-button
      >
      <base-button buttonType="primary">評量考核表規劃與審核</base-button>
      <base-button buttonType="primary" :disabled="true" class="margin"
        >評量表規劃</base-button
      >
      <base-button buttonType="primary" :disabled="true" class="margin"
        >評量表審核</base-button
      >
    </div>
  </template>
  <template v-else-if="routerName === 'assessment'">
    <div class="container">
      <base-button buttonType="primary" @click="navigateTo('course-table-list')"
        >查看課程詳細資料</base-button
      >
      <base-button buttonType="primary">評量考核題目設計</base-button>
      <base-button buttonType="primary">評量考核表規劃與審核</base-button>
    </div>
  </template>
  <router-view />
</template>

<script>
  import { ref, watch, onMounted } from "vue";
  import { useRouter, useRoute } from "vue-router";

  export default {
    setup() {
      // 路由與名稱
      const router = useRouter();
      const route = useRoute();
      const routerName = ref(route.name);

      // 路由變化監聽
      watch(
        () => route.name,
        (newRouteName) => {
          routerName.value = newRouteName;
        }
      );

      // 初始化 routerName
      onMounted(() => {
        routerName.value = route.name;
      });

      // 跳轉到目標路由
      const navigateTo = (routeName) => {
        router.push({ name: routeName });
      };

      return {
        routerName,
        navigateTo,
      };
    },
  };
</script>

<style scoped>
  .container {
    display: flex;
    align-items: flex-start;
  }

  .container button {
    margin-bottom: 10px;
    margin-right: 22px;
  }

  .margin {
    margin-top: 10px;
  }
</style>
