<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="login-container">
        <div class="login-card">
          <div class="login-header">
            <h2>Willkommen zurück</h2>
            <p>Melde dich an, um fortzufahren</p>
          </div>

          <ion-item class="custom-input" lines="none">
            <ion-label position="stacked">Benutzername</ion-label>
            <ion-input
              type="text"
              placeholder="dein Benutzername"
              v-model="username"
              @keyup.enter="handleLogin"
            />
          </ion-item>

          <ion-item class="custom-input" lines="none">
            <ion-label position="stacked">Passwort</ion-label>
            <ion-input
              type="password"
              placeholder="••••••••"
              v-model="password"
              @keyup.enter="handleLogin"
            />
          </ion-item>

          <ion-button
            expand="block"
            class="login-btn"
            :disabled="loading"
            @click="handleLogin"
          >
            <ion-spinner v-if="loading" name="crescent" />
            <span v-else>Anmelden</span>
          </ion-button>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  IonPage,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonSpinner,
} from '@ionic/vue';

import UserService from '@/services/UserService';
import ToastService from '@/services/general/ToastService';
import localizationService from '@/services/general/LocalizationService';

const router = useRouter();

const username = ref('');
const password = ref('');
const loading = ref(false);

function t(key: string, fallback: string) {
  return localizationService.t(key, undefined, fallback);
}

async function handleLogin() {
  if (!username.value || !password.value) {
    ToastService.showError(t('auth.missing_fields', 'Please fill in all fields.'));
    return;
  }

  loading.value = true;
  try {
    await UserService.login({ username: username.value, password: password.value });
    router.replace({ name: 'Home' });
  } catch {
    // Error toast is already shown by BaseService.handleRequest
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
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

.login-btn {
  --border-radius: 8px;
  font-weight: 600;
  margin-top: 1.5rem;
}
</style>
