<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="login-container">
        <div class="login-card">
          <div class="login-header">
            <h2>{{ isRegisterMode ? 'Konto erstellen' : 'Willkommen zurück' }}</h2>
            <p>{{ isRegisterMode ? 'Registriere dich, um zu starten' : 'Melde dich an, um fortzufahren' }}</p>
          </div>

          <form @submit.prevent="isRegisterMode ? handleRegister() : handleLogin()" @keydown="handleEnterKey">
            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Username</ion-label>
              <ion-input
                type="text"
                placeholder="dein Benutzername"
                v-model="username"
              ></ion-input>
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Passwort</ion-label>
              <ion-input
                :type="showPassword ? 'text' : 'password'"
                placeholder="••••••••"
                v-model="password"
              ></ion-input>
              </ion-item>

            <div class="forgot-password" v-if="!isRegisterMode">
              <a href="#">Passwort vergessen?</a>
            </div>

            <ion-button expand="block" type="submit" class="login-btn" :disabled="loading">
              <ion-spinner v-if="loading" name="crescent"></ion-spinner>
              <span v-else>{{ isRegisterMode ? 'Registrieren' : 'Anmelden' }}</span>
            </ion-button>
          </form>

          <div class="divider">
            <span>oder</span>
          </div>

          <div class="signup-link">
            {{ isRegisterMode ? 'Bereits ein Konto?' : 'Noch kein Konto?' }}
            <a href="#" @click.prevent="toggle('isRegisterMode')">
              {{ isRegisterMode ? 'Anmelden' : 'Registrieren' }}
            </a>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import {
  IonPage,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonIcon,
  IonSpinner,
} from "@ionic/vue";
import { logoGoogle, logoApple } from "ionicons/icons";

import UserService from "@/services/UserService";
import localizationService from "@/services/general/LocalizationService";
import ToastService from "@/services/general/ToastService";

export default defineComponent({
  name: "LoginPage",
  components: {
    IonPage,
    IonContent,
    IonItem,
    IonLabel,
    IonInput,
    IonButton,
    IonIcon,
    IonSpinner,
  },
  data() {
    return {
      username: "",
      password: "",
      // Added missing state properties
      loading: false,
      isRegisterMode: false,
      showPassword: false,
      // Icons
      logoGoogle,
      logoApple,
    };
  },
  methods: {
    t(key: string, vars?: Record<string, string | number>, fallback?: string) {
      return localizationService.t(key, vars, fallback);
    },

    showAuthError(error: { key: string; fallback: string }) {
      return ToastService.showError(
        this.t(error.key, undefined, error.fallback)
      );
    },

    toggle(flag: "showPassword" | "isRegisterMode") {
      if (flag === "showPassword") this.showPassword = !this.showPassword;
      if (flag === "isRegisterMode") this.isRegisterMode = !this.isRegisterMode;
    },

    handleEnterKey(event: KeyboardEvent) {
      if (event.key === "Enter") {
        this.isRegisterMode ? this.handleRegister() : this.handleLogin();
      }
    },

    async runAuth<T>(
      action: () => Promise<T>,
      error: { key: string; fallback: string }
    ) {
      this.loading = true;
      try {
        await action();
        this.redirectUser();
      } catch (err) {
        this.showAuthError(error);
      } finally {
        this.loading = false;
      }
    },

    async handleLogin() {
      if (!this.username || !this.password) {
        return this.showAuthError({
          key: "auth.missing_fields",
          fallback: "Please fill in all the fields.",
        });
      }

      await this.runAuth(
        () =>
          UserService.login({
            username: this.username,
            password: this.password,
          }),
        {
          key: "auth.invalid_credentials",
          fallback: "Invalid username or password.",
        }
      );
    },

    async handleRegister() {
      if (!this.username || !this.password) {
        return this.showAuthError({
          key: "auth.missing_fields",
          fallback: "Please fill in all the fields.",
        });
      }

      await this.runAuth(
        () =>
          UserService.register({
            username: this.username,
            password: this.password,
          }),
        {
          key: "auth.registration_failed",
          fallback: "Could not create account.",
        }
      );
    },

    redirectUser() {
      this.$router.replace({ name: "home" });
    },
  },
});
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  background: var(--ion-background-color);
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: var(--ion-card-background);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--ion-text-color);
}

.login-header p {
  color: var(--ion-color-medium);
}

.custom-input {
  --background: rgba(255, 255, 255, 0.05);
  --border-radius: 8px;
  margin-bottom: 1rem;
  --padding-start: 1rem;
}

.custom-input ion-label {
  color: var(--ion-color-medium) !important;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.forgot-password {
  text-align: right;
  margin-bottom: 1.5rem;
}

.forgot-password a {
  color: var(--ion-color-primary);
  font-size: 0.9rem;
  text-decoration: none;
}

.login-btn {
  --border-radius: 8px;
  font-weight: 600;
  margin-bottom: 1.5rem;
  --background: var(--ion-color-primary);
  --color: var(--ion-color-primary-contrast);
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--ion-color-medium);
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.divider span {
  padding: 0 10px;
  font-size: 0.9rem;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.social-btn {
  --border-radius: 8px;
  --border-color: rgba(255, 255, 255, 0.1);
  --color: var(--ion-text-color);
  font-size: 0.9rem;
}

.signup-link {
  text-align: center;
  font-size: 0.9rem;
  color: var(--ion-color-medium);
}

.signup-link a {
  color: var(--ion-color-primary);
  text-decoration: none;
  font-weight: 600;
  margin-left: 5px;
}
</style>