<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="dark">
        <ion-title>SkillPlate</ion-title>

        <ion-buttons slot="end">
          <ion-button router-link="/home">Home</ion-button>
          <ion-button router-link="/courses">Kurse</ion-button>
          <ion-button router-link="/generate">
            <ion-icon slot="start" :icon="sparkles" style="margin-right: 5px;" />
            AI Generator
          </ion-button>

          <!-- Auth-aware button -->
          <template v-if="isAuthenticated">
            <ion-button fill="outline" color="medium" @click="handleLogout">
              <ion-spinner v-if="loggingOut" name="crescent" />
              <span v-else>Abmelden</span>
            </ion-button>
          </template>
          <template v-else>
            <ion-button router-link="/login" color="primary" fill="solid">Login</ion-button>
          </template>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-router-outlet />
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
  IonPage,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonButtons,
  IonButton,
  IonRouterOutlet,
  IonIcon,
  IonSpinner,
} from '@ionic/vue';
import { sparkles } from 'ionicons/icons';

import UserService from '@/services/UserService';

const isAuthenticated = ref(false);
const loggingOut = ref(false);

onMounted(async () => {
  isAuthenticated.value = await UserService.isAuthenticated();
});

async function handleLogout() {
  loggingOut.value = true;
  try {
    await UserService.logout();
    isAuthenticated.value = false;
  } finally {
    loggingOut.value = false;
  }
}
</script>
