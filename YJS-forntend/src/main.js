import { createApp } from "vue";
import ContentManager from "./components/ContentManager.vue";
import BaseButton from "./components/Button/BaseButton.vue";
import SideBar from "./components/SideBar.vue";
import NavBar from "./components/NavBar.vue";
import App from "./App.vue";

const app = createApp(App);
app.component("content-manager", ContentManager);
app.component("base-button", BaseButton);
app.component("side-bar", SideBar);
app.component("nav-bar", NavBar);

app.mount("#app");
