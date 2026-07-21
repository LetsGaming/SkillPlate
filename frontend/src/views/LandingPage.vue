<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="landing-container">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="hero-content">
            <h1 class="animate-fade-in-up">Meistere die Kunst des Kochens</h1>
            <p class="animate-fade-in-up delay-1">
              Entdecke exklusive Kochkurse und werde zum Profi in deiner eigenen Küche.
            </p>
            <div class="hero-actions animate-fade-in-up delay-2">
              <ion-button size="large" color="primary" router-link="/courses">
                Kurse entdecken
                <ion-icon slot="end" :icon="arrowForwardOutline"></ion-icon>
              </ion-button>
            </div>
          </div>
          <div class="hero-overlay"></div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
          <div class="feature-card">
            <ion-icon :icon="restaurantOutline" color="primary"></ion-icon>
            <h3>Profiköche</h3>
            <p>Lerne von den Besten der Branche in interaktiven Sessions.</p>
          </div>
          <div class="feature-card">
            <ion-icon :icon="globeOutline" color="primary"></ion-icon>
            <h3>Hybrid</h3>
            <p>Nimm vor Ort teil oder schalte dich bequem von zuhause dazu.</p>
          </div>
          <div class="feature-card">
            <ion-icon :icon="ribbonOutline" color="primary"></ion-icon>
            <h3>Zertifiziert</h3>
            <p>Erhalte anerkannte Zertifikate für deinen Fortschritt.</p>
          </div>
        </section>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonPage, IonContent, IonButton, IonIcon } from '@ionic/vue';
import { arrowForwardOutline, restaurantOutline, globeOutline, ribbonOutline } from 'ionicons/icons';
</script>

<style scoped>
.landing-container {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  background-color: var(--ion-background-color);
}

/* Hero Section */
.hero-section {
  position: relative;
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: url('https://images.unsplash.com/photo-1556910103-1c02745a30bf?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80') no-repeat center center;
  background-size: cover;
  padding: 2rem;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0,0,0,0.3), var(--ion-background-color));
  z-index: 1;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 800px;
}

.hero-content h1 {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #fff;
  text-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

.hero-content p {
  font-size: 1.5rem;
  color: #e0e0e0;
  margin-bottom: 2rem;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* Features Section */
.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 2;
}

.feature-card {
  background: var(--ion-card-background);
  padding: 2rem;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px -10px rgba(0,0,0,0.6);
  border-color: var(--ion-color-primary);
}

.feature-card ion-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--ion-text-color);
}

.feature-card p {
  color: var(--ion-color-medium);
  line-height: 1.6;
}

/* Animations */
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

.delay-1 { animation-delay: 0.2s; }
.delay-2 { animation-delay: 0.4s; }

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Overrides */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2.5rem;
  }
  .hero-content p {
    font-size: 1.1rem;
  }
}
</style>
