import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

import { library } from "@fortawesome/fontawesome-svg-core";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import {
  faDragon,
  faWandMagicSparkles,
  faSpinner,
  faLightbulb,
} from "@fortawesome/free-solid-svg-icons";

library.add(faDragon, faWandMagicSparkles, faSpinner, faLightbulb);

import 'bootstrap/dist/css/bootstrap.min.css'
import 'vue-multiselect/dist/vue-multiselect.css';
import 'bootstrap'

const app = createApp(App);
app.component("font-awesome-icon", FontAwesomeIcon);

app.mount("#app");