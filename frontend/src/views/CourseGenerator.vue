<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="generator-container">
        <h1>Kurs-Generator</h1>
        <p class="subtitle">Lass die KI deinen perfekten Kochkurs erstellen.</p>

        <div class="generator-card">
          <form @submit.prevent="generateCourse" v-if="!generatedCourse">
            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Thema</ion-label>
              <ion-input v-model="topic" placeholder="z.B. Italienische Pasta, Vegan für Einsteiger"></ion-input>
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Schwierigkeit</ion-label>
              <ion-select v-model="difficulty" placeholder="Wähle eine Stufe">
                <ion-select-option value="beginner">Anfänger</ion-select-option>
                <ion-select-option value="intermediate">Fortgeschritten</ion-select-option>
                <ion-select-option value="expert">Profi</ion-select-option>
              </ion-select>
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Dauer (Wochen)</ion-label>
              <ion-input type="number" v-model="duration" placeholder="4"></ion-input>
            </ion-item>

            <ion-button expand="block" type="submit" class="generate-btn" :disabled="isLoading">
              <span v-if="!isLoading">Kurs erstellen</span>
              <ion-spinner v-else name="crescent"></ion-spinner>
            </ion-button>
          </form>

          <div v-else class="result-view animate-fade-in">
            <div class="success-header">
              <ion-icon :icon="checkmarkCircle" color="success"></ion-icon>
              <h2>Dein Kurs ist fertig!</h2>
            </div>
            
            <div class="course-preview">
              <h3>{{ topic || 'Dein Kurs' }}</h3>
              <div class="meta-tags">
                <ion-chip color="primary">{{ difficulty }}</ion-chip>
                <ion-chip>{{ duration }} Wochen</ion-chip>
              </div>
              <p>Dieser maßgeschneiderte Kurs führt dich in die Welt von {{ topic }} ein. Lerne Schritt für Schritt von den Grundlagen bis zu meisterhaften Kreationen.</p>
              
              <div class="preview-actions">
                <ion-button fill="outline" @click="generatedCourse = false">Zurück</ion-button>
                <ion-button color="primary">In den Kalender & Zertifikat starten</ion-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { IonPage, IonContent, IonItem, IonLabel, IonInput, IonButton, IonSelect, IonSelectOption, IonSpinner, IonIcon, IonChip } from '@ionic/vue';
import { checkmarkCircle } from 'ionicons/icons';

const topic = ref('');
const difficulty = ref('');
const duration = ref('');
const isLoading = ref(false);
const generatedCourse = ref(false);

const generateCourse = () => {
  isLoading.value = true;
  // Mock API call
  setTimeout(() => {
    isLoading.value = false;
    generatedCourse.value = true;
  }, 2000);
};
</script>

<style scoped>
.generator-container {
  padding: 2rem;
  max-width: 800px;
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
  margin-bottom: 3rem;
  font-size: 1.1rem;
}

.generator-card {
  background: var(--ion-card-background);
  padding: 2rem;
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.custom-input {
  --background: rgba(255, 255, 255, 0.05);
  --border-radius: 8px;
  margin-bottom: 1.5rem;
  --padding-start: 1rem;
}

.generate-btn {
  margin-top: 2rem;
  --background: var(--ion-color-primary);
  --color: black;
  font-weight: 700;
}

.result-view {
  text-align: center;
}

.success-header ion-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.course-preview {
  background: rgba(255, 255, 255, 0.03);
  padding: 1.5rem;
  border-radius: 12px;
  margin-top: 2rem;
  text-align: left;
}

.course-preview h3 {
  color: var(--ion-color-primary);
  margin-top: 0;
}

.preview-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 2rem;
  gap: 1rem;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
