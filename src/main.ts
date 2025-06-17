// VUE
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

// BOOTSTRAP
import { createBootstrap } from "bootstrap-vue-next";
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue-next/dist/bootstrap-vue-next.css";

// DEV CHANGES
import "./style.css";
import './styles/custom-bootstrap.scss';

// BUILD
createApp(App).use(router).use(createBootstrap()).mount("#app");
