import { createApp } from "vue";
import BaseButton from "./components/Button/BaseButton.vue";
import NavBar from "@/components/NavBar.vue";
import SideBar from "./components/SideBar.vue";
import Breadcrumbs from "./components/Breadcrumbs.vue";
import router from "@/router";

import App from "./App.vue";

const app = createApp(App);

app.use(router);
app.component("nav-bar", NavBar);
app.component("side-bar", SideBar);
app.component("breadcrumbs", Breadcrumbs);
app.component("base-button", BaseButton);

app.mount("#app");
