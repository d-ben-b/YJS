import { createRouter, createWebHistory } from "vue-router";
import TrainContent from "@/views/TrainContent.vue";
import CourseTable from "@/views/CourseTable.vue";
import NotFoundComponent from "@/components/NotFoundComponent.vue";
import Content from "@/views/Content.vue";

const routes = [
  { path: "/", component: "", meta: { breadcrumb: "首頁" } },
  {
    path: "/:pathMatch(.*)*",
    component: NotFoundComponent,
    meta: { breadcrumb: "404" },
  },
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
        children: [
          {
            path: "course-table",
            name: "course-table",
            component: CourseTable,
            meta: { breadcrumb: "課程維護" },
          },
        ],
      },
      {
        path: "quiz",
        name: "quiz",
        component: Content,
        meta: { breadcrumb: "隨堂測驗內容" },
        children: [
          {
            path: "course-table-view",
            name: "course-table-view",
            component: CourseTable,
            meta: { breadcrumb: "查看課程列表" },
          },
        ],
      },
      {
        path: "assessment",
        name: "assessment",
        component: Content,
        meta: { breadcrumb: "評量考核內容" },
        children: [
          {
            path: "course-table-list",
            name: "course-table-list",
            component: CourseTable,
            meta: { breadcrumb: "查看課程列表" },
          },
        ],
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
