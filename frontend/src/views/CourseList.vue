<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="courses-container">
        <h1>Unsere Kochkurse</h1>
        <p class="subtitle">Wähle aus einer Vielzahl von professionellen Kursen.</p>

        <!-- Loading -->
        <div v-if="isLoading" class="state-message">
          <ion-spinner name="crescent" />
          <p>Kurse werden geladen…</p>
        </div>

        <!-- Error -->
        <div v-else-if="error" class="state-message state-error">
          <ion-icon :icon="alertCircleOutline" />
          <p>{{ error }}</p>
          <ion-button fill="outline" @click="loadCourse">Erneut versuchen</ion-button>
        </div>

        <!-- Course detail (backend currently returns a single course by ID) -->
        <div v-else-if="course" class="course-detail">
          <ion-card class="course-card">
            <ion-card-header>
              <ion-card-subtitle>
                <ion-chip color="primary">{{ course.difficulty }}</ion-chip>
                <ion-chip :color="course.online ? 'success' : 'warning'">
                  {{ course.online ? 'Online' : 'Vor-Ort' }}
                </ion-chip>
              </ion-card-subtitle>
              <ion-card-title>{{ course.theme }}</ion-card-title>
            </ion-card-header>

            <ion-card-content>
              <p class="duration-label">Dauer: {{ course.duration }} Wochen</p>

              <div
                v-for="recipe in course.recipes"
                :key="recipe.recipe_name"
                class="recipe-item"
              >
                <h3>{{ recipe.recipe_name }}</h3>
                <p class="instructions">{{ recipe.recipe_instructions }}</p>
                <ul class="ingredients">
                  <li
                    v-for="ing in recipe.ingredients"
                    :key="ing.ingredient_name"
                  >
                    {{ ing.amount }} {{ ing.unit }} — {{ ing.ingredient_name }}
                    <span class="ing-type">({{ ing.ingredient_type }})</span>
                  </li>
                </ul>
              </div>
            </ion-card-content>
          </ion-card>
        </div>

        <!-- Empty state -->
        <div v-else class="state-message">
          <p>Kein Kurs verfügbar. Erstelle zuerst einen im KI-Generator.</p>
          <ion-button router-link="/generate" color="primary">Zum Generator</ion-button>
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import {
  IonPage,
  IonContent,
  IonCard,
  IonCardHeader,
  IonCardSubtitle,
  IonCardTitle,
  IonCardContent,
  IonButton,
  IonSpinner,
  IonIcon,
  IonChip,
} from '@ionic/vue';
import { alertCircleOutline } from 'ionicons/icons';

import CourseService from '@/services/CourseService';

// The backend's GET /api/course currently returns { courseId } for a demo lookup.
// We use a known demo ID here; swap this out once the backend persists real courses.
const DEMO_COURSE_ID = 'demo';

const isLoading = ref(false);
const error = ref<string | null>(null);
const course = ref<Course | null>(null);

async function loadCourse() {
  isLoading.value = true;
  error.value = null;
  try {
    // Once the backend stores full courses, this will return a full Course object.
    // For now the endpoint only echoes back the ID, so we show the empty state.
    await CourseService.getCourse(DEMO_COURSE_ID);
    // course.value = result; // uncomment when backend returns full course data
  } catch (err: any) {
    error.value = err?.message ?? 'Unbekannter Fehler';
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadCourse);
</script>

<style scoped>
.courses-container {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: var(--ion-color-medium);
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.state-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem 1rem;
  color: var(--ion-color-medium);
  text-align: center;
}

.state-message ion-spinner,
.state-message ion-icon {
  font-size: 2.5rem;
}

.state-error ion-icon {
  color: var(--ion-color-danger);
}

.course-card {
  border-radius: 12px;
  background: var(--ion-card-background);
}

.duration-label {
  color: var(--ion-color-medium);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.recipe-item {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  border-left: 3px solid var(--ion-color-primary);
}

.recipe-item h3 {
  margin-top: 0;
  color: var(--ion-color-primary);
}

.instructions {
  font-size: 0.9rem;
  color: var(--ion-color-medium);
}

.ingredients {
  padding-left: 1.2rem;
  font-size: 0.9rem;
  color: var(--ion-color-medium);
}

.ing-type {
  font-style: italic;
  opacity: 0.7;
}
</style>
