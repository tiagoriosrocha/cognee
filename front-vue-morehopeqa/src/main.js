import { createApp } from "vue";
import App from "./App.vue";
import store from "./store";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";

import VNetworkGraph from "v-network-graph";
import "v-network-graph/lib/style.css";

//import { forceLayout } from "v-network-graph";
//VNetworkGraph.useLayout("force", forceLayout);

loadFonts();

createApp(App).use(store).use(VNetworkGraph).use(vuetify).mount("#app");
