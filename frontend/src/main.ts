import { createApp } from 'vue'
import App from './App.vue'
import router from './router';

import { IonicVue } from '@ionic/vue';

/* Core CSS required for Ionic components to work properly */
import '@ionic/vue/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/vue/css/normalize.css';
import '@ionic/vue/css/structure.css';
import '@ionic/vue/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/vue/css/padding.css';
import '@ionic/vue/css/float-elements.css';
import '@ionic/vue/css/text-alignment.css';
import '@ionic/vue/css/text-transformation.css';
import '@ionic/vue/css/flex-utils.css';
import '@ionic/vue/css/display.css';

/**
 * Ionic Dark Mode
 * -----------------------------------------------------
 * For more info, please see:
 * https://ionicframework.com/docs/theming/dark-mode
 */

/* @import '@ionic/vue/css/palettes/dark.always.css'; */
/* @import '@ionic/vue/css/palettes/dark.class.css'; */
import '@ionic/vue/css/palettes/dark.system.css';

/* Theme variables */
import './theme/variables.css';


/* Services */
import Utils from "./utils/Utils";
import localizationService from "@/services/general/LocalizationService";

/**
 * Auto-register locale loaders from the `src/locales` directory.
 * Uses Vite's `import.meta.glob` to maintain code-splitting (lazy-loading).
 * Only the required language bundle is downloaded on startup.
 */
const localeLoaders = import.meta.glob("./locales/*.{ts,js}");

for (const path in localeLoaders) {
  const loader = localeLoaders[path] as () => Promise<any>;
  const match = path.match(/\.\/locales\/([^\.\/]+)\./);

  if (match) {
    const localeKey = match[1];
    localizationService.registerLoader(localeKey, () =>
      loader().then((mod) => mod.default),
    );
  }
}

async function initializeApp() {
  document.title = Utils.getAppTitle();
  const app = createApp(App).use(IonicVue).use(router);

  // We provide the service globally
  app.config.globalProperties.$i18n = localizationService;

  // We create a global helper that explicitly depends on the reactive locale
  app.config.globalProperties.$t = (
    key: string,
    vars?: any,
    fallback?: string,
  ) => {
    // Accessing .value here registers this function in Vue's dependency tracker
    const _ = localizationService.locale.value;
    return localizationService.t(key, vars, fallback);
  };

  await Promise.all([
    router.isReady(),
    localizationService.resolveInitialLocale(),
  ]);

  app.mount("#app");
}

initializeApp();