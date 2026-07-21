<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="generator-container">
        <h1>Kurs-Generator</h1>
        <p class="subtitle">Lass die KI deinen perfekten Kochkurs erstellen.</p>

        <div class="generator-card">
          <!-- Form -->
          <template v-if="!generatedCourse">
            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Thema</ion-label>
              <ion-input
                v-model="form.theme"
                placeholder="z.B. Italienische Pasta, Vegan für Einsteiger"
              />
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Schwierigkeit</ion-label>
              <ion-select v-model="form.difficulty" placeholder="Wähle eine Stufe">
                <ion-select-option value="Easy">Anfänger</ion-select-option>
                <ion-select-option value="Medium">Fortgeschritten</ion-select-option>
                <ion-select-option value="Pro">Profi</ion-select-option>
              </ion-select>
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Dauer (Wochen)</ion-label>
              <ion-input type="number" v-model.number="form.duration" placeholder="4" />
            </ion-item>

            <ion-item class="custom-input" lines="none">
              <ion-label position="stacked">Format</ion-label>
              <ion-select v-model="form.online" placeholder="Online oder Vor-Ort?">
                <ion-select-option :value="true">Online</ion-select-option>
                <ion-select-option :value="false">Vor-Ort</ion-select-option>
              </ion-select>
            </ion-item>

            <ion-button
              expand="block"
              class="generate-btn"
              :disabled="isLoading || !isFormValid"
              @click="generateCourse"
            >
              <span v-if="!isLoading">Kurs erstellen</span>
              <ion-spinner v-else name="crescent" />
            </ion-button>
          </template>

          <!-- Result -->
          <div v-else class="result-view animate-fade-in">
            <div class="success-header">
              <ion-icon :icon="checkmarkCircle" color="success" />
              <h2>Dein Kurs ist fertig!</h2>
            </div>

            <div class="course-preview">
              <h3>{{ generatedCourse.theme }}</h3>

              <div class="meta-tags">
                <ion-chip color="primary">{{ generatedCourse.difficulty }}</ion-chip>
                <ion-chip>{{ generatedCourse.duration }} Wochen</ion-chip>
                <ion-chip :color="generatedCourse.online ? 'success' : 'warning'">
                  {{ generatedCourse.online ? 'Online' : 'Vor-Ort' }}
                </ion-chip>
              </div>

              <p class="recipe-count">
                {{ generatedCourse.recipes.length }} Rezept(e) enthalten
              </p>

              <div v-if="generatedCourse.recipes.length" class="recipe-list">
                <div
                  v-for="recipe in generatedCourse.recipes"
                  :key="recipe.recipe_name"
                  class="recipe-item"
                >
                  <strong>{{ recipe.recipe_name }}</strong>
                  <p>{{ recipe.recipe_instructions }}</p>
                  <ul class="ingredients">
                    <li v-for="ing in recipe.ingredients" :key="ing.ingredient_name">
                      {{ ing.amount }} {{ ing.unit }} {{ ing.ingredient_name }}
                    </li>
                  </ul>
                </div>
              </div>

              <div class="preview-actions">
                <ion-button fill="outline" @click="resetForm">Neu erstellen</ion-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import {
  IonPage,
  IonContent,
  IonItem,
  IonLabel,
  IonInput,
  IonButton,
  IonSelect,
  IonSelectOption,
  IonSpinner,
  IonIcon,
  IonChip,
} from '@ionic/vue';
import { checkmarkCircle } from 'ionicons/icons';

import CourseService from '@/services/CourseService';

interface CourseForm {
  theme: string;
  difficulty: string;
  duration: number | null;
  online: boolean | null;
}

const form = ref<CourseForm>({
  theme: '',
  difficulty: '',
  duration: null,
  online: null,
});

const isLoading = ref(false);
const generatedCourse = ref<Course | null>(null);

const isFormValid = computed(
  () =>
    form.value.theme.trim() &&
    form.value.difficulty &&
    form.value.duration !== null &&
    form.value.duration > 0 &&
    form.value.online !== null,
);

async function generateCourse() {
  if (!isFormValid.value) return;

  isLoading.value = true;
  try {
    generatedCourse.value = await CourseService.generateCourse({
      theme: form.value.theme,
      difficulty: form.value.difficulty,
      duration: form.value.duration!,
      online: form.value.online!,
    });
  } finally {
    isLoading.value = false;
  }
}

function resetForm() {
  generatedCourse.value = null;
  form.value = { theme: '', difficulty: '', duration: null, online: null };
}
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

.meta-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.recipe-count {
  color: var(--ion-color-medium);
  font-size: 0.95rem;
}

.recipe-list {
  margin-top: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.recipe-item {
  background: rgba(255, 255, 255, 0.04);
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid var(--ion-color-primary);
}

.recipe-item strong {
  font-size: 1.05rem;
}

.recipe-item p {
  color: var(--ion-color-medium);
  font-size: 0.9rem;
  margin: 0.5rem 0;
}

.ingredients {
  margin: 0.5rem 0 0;
  padding-left: 1.2rem;
  font-size: 0.9rem;
  color: var(--ion-color-medium);
}

.preview-actions {
  margin-top: 2rem;
  display: flex;
  justify-content: flex-end;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}
</style>
