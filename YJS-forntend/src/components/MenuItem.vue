<template>
  <li>
    <div class="menu-item" :class="isOpen" @click="handleClick">
      <i v-if="hasChildren" :class="iconClass"></i> {{ item.title }}
    </div>
    <ul v-if="hasChildren && item.open">
      <MenuItem
        v-for="child in item.children"
        :key="child.id"
        :item="child"
        @select-item="
          (id, path) => emitSelectItem(id, [...path, item.title])
        " />
    </ul>
  </li>
</template>

<script setup>
  import { computed } from "vue";
  import MenuItem from "./MenuItem.vue";

  const props = defineProps({
    item: {
      type: Object,
      required: true,
    },
  });

  const emit = defineEmits(["select-item"]);

  const hasChildren = computed(
    () => props.item.children && props.item.children.length > 0
  );

  const iconClass = computed(() => {
    if (hasChildren.value) {
      return props.item.open ? "fas fa-folder-open" : "fas fa-folder";
    }
    return "fas fa-file";
  });

  const isOpen = computed(() => (props.item.open ? "open" : "close"));

  const handleClick = () => {
    if (!hasChildren.value) {
      emit("select-item", props.item.id, [props.item.title]);
    } else {
      props.item.open = !props.item.open;
    }
  };

  const emitSelectItem = (id, path) => {
    emit("select-item", id, path);
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
