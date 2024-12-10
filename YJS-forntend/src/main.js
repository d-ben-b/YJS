import { createApp } from "vue";
import BaseButton from "./components/Button/BaseButton.vue";
import NavBar from "@/components/NavBar.vue";
import SideBar from "./components/SideBar.vue";
import Breadcrumbs from "./components/Breadcrumbs.vue";
import router from "@/router";
import axios from "axios";

import App from "./App.vue";

axios.defaults.baseURL = "http://127.0.0.1:5000"; // 根據你的 Flask API 地址進行修改
const app = createApp(App);

app.use(router);
app.config.globalProperties.$axios = axios;
app.component("nav-bar", NavBar);
app.component("side-bar", SideBar);
app.component("breadcrumbs", Breadcrumbs);
app.component("base-button", BaseButton);

app.mount("#app");
