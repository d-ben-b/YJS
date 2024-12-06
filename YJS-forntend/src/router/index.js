import { createRouter, createWebHistory } from "vue-router";
import ContentManager from "@/components/TrainContent.vue";

const routes = [
  { path: "/", component: ContentManager },
  { path: "/training-content", component: ContentManager },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
