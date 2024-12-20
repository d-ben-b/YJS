<template>
  <li>
    <div class="menu-item" :class="isOpen" @click="toggle">
      <i v-if="hasChildren" :class="iconClass"></i> {{ item.title }}
    </div>
    <ul v-if="hasChildren && item.open">
      <MenuItem v-for="child in item.children" :key="child.id" :item="child" />
    </ul>
  </li>
</template>

<script setup>
  import { defineProps, computed } from "vue";
  import MenuItem from "./MenuItem.vue"; // 遞迴引入自己

  const props = defineProps({
    item: {
      type: Object,
      required: true,
    },
  });

  const hasChildren = computed(() => {
    return props.item.children && props.item.children.length > 0;
  });

  // 設定圖示類別，根據是否有子項目決定
  const iconClass = computed(() => {
    if (hasChildren.value) {
      return props.item.open ? "fas fa-folder-open" : "fas fa-folder";
    }
    return "fas fa-file";
  });

  const isOpen = computed(() => {
    if (props.item.open) {
      return props.item.open ? "open" : "close";
    }
    return "close";
  });

  // 切換展開狀態
  const toggle = () => {
    if (hasChildren.value) {
      if (!props.item.hasOwnProperty("open")) {
        props.item.open = false;
      }
      props.item.open = !props.item.open;
    }
  };
</script>

<style scoped>
  .menu-item {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-weight: bold;
    margin: 8px 0;
    padding: 5px;
    border-radius: 4px;
    transition: background-color 0.3s, color 0.3s;
  }

  .menu-item i {
    margin-right: 10px;
    font-size: 14px;
    color: #6c757d;
  }

  .menu-item:hover {
    color: #0056b3;
    background-color: #f0f8ff;
  }

  .menu-item::before {
    content: ">";
    margin-right: 8px;
    font-size: 12px;
    color: #6c757d;
    transition: transform 0.3s;
  }

  .menu-item.open::before {
    transform: rotate(90deg) translateY(-1px);
  }

  ul {
    list-style: none;
    padding-left: 20px;
    margin: 0;
    border-left: 2px solid #e0e0e0;
  }

  li {
    margin-bottom: 8px;
  }

  li:last-child {
    margin-bottom: 0;
  }
</style>
