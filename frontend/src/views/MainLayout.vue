<template>
  <ion-page>
    <ion-header>
      <ion-toolbar color="dark">
        <ion-buttons slot="start">
          <ion-menu-button></ion-menu-button>
        </ion-buttons>
        <ion-title>SkillPlate</ion-title>
        <ion-buttons slot="end">
          <ion-button router-link="/home">Home</ion-button>
          <ion-button router-link="/courses">Kurse</ion-button>
          <ion-button router-link="/generate">
            <ion-icon slot="start" :icon="sparkles" style="margin-right: 5px;"></ion-icon>
            AI Generator
          </ion-button>
          <ion-button router-link="/login" color="primary" fill="solid">Login</ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-router-outlet></ion-router-outlet>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonHeader, IonToolbar, IonTitle, IonContent, IonButtons, IonMenuButton, IonButton, IonRouterOutlet, IonIcon } from '@ionic/vue';
import { sparkles } from 'ionicons/icons';
</script>
