// Styles
import "@mdi/font/css/materialdesignicons.css"; // MDI
import "@fortawesome/fontawesome-free/css/all.css"; // Font Awesome
import "vuetify/styles";

// Vuetify
import { createVuetify } from "vuetify";

// Importa sets de ícones
import { aliases, mdi } from "vuetify/iconsets/mdi";
import { fa } from "vuetify/iconsets/fa";

export default createVuetify({
  icons: {
    defaultSet: "fa", // fa ou mdi
    aliases,
    sets: {
      mdi, // Material Design Icons
      fa, // Font Awesome
    },
  },
});
