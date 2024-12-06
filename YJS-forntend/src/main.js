import { createApp } from "vue";
import BaseButton from "./components/Button/BaseButton.vue";
import router from "@/router";

import App from "./App.vue";

const app = createApp(App);

app.use(router);
app.component("base-button", BaseButton);

app.mount("#app");
