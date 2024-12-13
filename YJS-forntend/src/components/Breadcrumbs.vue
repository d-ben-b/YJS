<template>
  <div class="breadcrumbs">
    <router-link to="/">首頁</router-link> /
    <span v-for="(crumb, index) in breadcrumbs" :key="index">
      <router-link v-if="index < breadcrumbs.length - 1" :to="crumb.path">{{
        crumb.name
      }}</router-link>
      <span v-else>{{ crumb.name }}</span>
      <span v-if="index < breadcrumbs.length - 1"> / </span>
    </span>
  </div>
</template>

<script>
  import { computed } from "vue";
  import { useRoute } from "vue-router";

  export default {
    setup() {
      const route = useRoute();

      // Computed property to generate breadcrumbs
      const breadcrumbs = computed(() => {
        const matched = route.matched;
        return matched.map((route) => {
          return {
            name: route.meta.breadcrumb || route.name,
            path: route.path === "/" ? "/" : route.path,
          };
        });
      });

      return {
        breadcrumbs,
      };
    },
  };
</script>

<style scoped>
  .breadcrumbs {
    width: max-content;
    position: relative;
    left: 45px;
    font-size: 16px;
    color: #555;
  }

  .breadcrumbs a {
    color: #007bff;
    text-decoration: none;
  }

  .breadcrumbs a:hover {
    text-decoration: underline;
  }
</style>
