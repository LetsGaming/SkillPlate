<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="courses-container">
        <h1>Unsere Kochkurse</h1>
        <p class="subtitle">Wähle aus einer Vielzahl von professionellen Kursen.</p>

        <div class="course-grid">
          <!-- Placeholder Data -->
          <ion-card v-for="i in 6" :key="i" class="course-card">
            <img :src="`https://source.unsplash.com/random/400x250?cooking,food&sig=${i}`" alt="Course Image" />
            <ion-card-header>
              <ion-card-subtitle>Anfänger</ion-card-subtitle>
              <ion-card-title>Grundlagen der Küche {{ i }}</ion-card-title>
            </ion-card-header>
            <ion-card-content>
              Lerne die essentiellen Techniken, die jeder Koch beherrschen muss.
            </ion-card-content>
            <div class="card-actions">
              <ion-button fill="clear">Details</ion-button>
              <ion-button color="primary">Buchen</ion-button>
            </div>
          </ion-card>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonCard, IonCardHeader, IonCardSubtitle, IonCardTitle, IonCardContent, IonButton } from '@ionic/vue';
</script>

<style scoped>
.courses-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: var(--ion-text-color);
}

.subtitle {
  color: var(--ion-color-medium);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.course-card {
  margin: 0;
  border-radius: 12px;
  overflow: hidden;
  transition: transform 0.3s ease;
  background: var(--ion-card-background);
}

.course-card:hover {
  transform: translateY(-5px);
}

.course-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  padding: 0 1rem 1rem;
}
</style>
