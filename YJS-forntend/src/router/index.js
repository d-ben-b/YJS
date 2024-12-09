import { createRouter, createWebHistory } from "vue-router";
import TrainContent from "@/views/TrainContent.vue";
import Content from "@/views/Content.vue";
import Quiz from "@/views/Quiz.vue";
import Assessment from "@/views/Assessment.vue";

const routes = [
  { path: "/", component: "", meta: { breadcrumb: "首頁" } },
  {
    path: "/training-content",
    component: TrainContent,
    name: "training-content",
    meta: { breadcrumb: "教育訓練內容管理" },
    children: [
      {
        path: "content",
        name: "content",
        component: Content,
        meta: { breadcrumb: "教育訓練內容" },
      },
      {
        path: "quiz",
        name: "quiz",
        component: Quiz,
        meta: { breadcrumb: "隨堂測驗內容" },
      },
      {
        path: "assessment",
        name: "assessment",
        component: Assessment,
        meta: { breadcrumb: "評量考核內容" },
      },
    ],
  },
  {
    path: "/training-content/content",
    component: Content,
    name: "Content",
    meta: { breadcrumb: "教育訓練內容" },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
