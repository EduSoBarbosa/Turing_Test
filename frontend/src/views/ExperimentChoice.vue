<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'

const router = useRouter()

const steps = ['Escolha', 'Respostas', 'Julgamento', 'Resultado']
const currentStep = 0

const options = [
  {
    id: 'novo',
    title: 'Novo experimento',
    description:
      'Responda às perguntas do zero. Sua resposta humana é pareada com uma resposta gerada por IA para o julgamento.',
    tags: ['Humano + IA', 'Respostas novas', '~10 min'],
    action: 'Começar novo experimento',
    href: '/quiz/novo/perguntas',
    recommended: true,
    variant: 'green'
  },
  {
    id: 'prontos',
    title: 'Questionários prontos',
    description:
      'Escolha um conjunto já respondido e vá direto para a etapa de julgamento, sem precisar responder nada.',
    tags: ['Respostas armazenadas', 'Direto ao julgamento', '~5 min'],
    action: 'Ver questionários',
    href: '/questionarios',
    recommended: false,
    variant: 'pink'
  }
]

const goTo = (href: string) => {
  router.push(href)
}
</script>

<template>
  <div class="app-shell">

    <AppSidebar active="novo" />

    <main class="content">

      <!-- TOP BAR -->
      <header class="topbar">

        <div class="breadcrumb">
          Experimento / <strong>Escolha</strong>
        </div>

        <ol class="steps">
          <template v-for="(step, index) in steps" :key="step">
            <li
              class="step"
              :class="{ active: index === currentStep }"
            >
              <span class="step-dot">{{ index + 1 }}</span>
              {{ step }}
            </li>
            <li
              v-if="index < steps.length - 1"
              class="step-line"
              aria-hidden="true"
            />
          </template>
        </ol>

        <span class="topbar-spacer" aria-hidden="true" />

      </header>

      <!-- BODY -->
      <section class="body">

        <span class="eyebrow">PASSO 1 DE 4</span>

        <h1>Como deseja participar?</h1>

        <p class="lead">
          Escolha entre responder as perguntas do zero ou julgar
          um conjunto de respostas que já foi preenchido.
        </p>

        <div class="cards">

          <article
            v-for="option in options"
            :key="option.id"
            class="card"
            :class="option.variant"
          >

            <span v-if="option.recommended" class="recommended">
              RECOMENDADO
            </span>

            <div class="badge">
              <svg
                v-if="option.id === 'novo'"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path d="M12 20h9M16.5 3.5a2.1 2.1 0 013 3L7 19l-4 1 1-4z" />
              </svg>

              <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                <rect x="4" y="3" width="16" height="18" rx="3" />
                <path d="M8 8h8M8 12h8M8 16h4" />
              </svg>
            </div>

            <h2>{{ option.title }}</h2>

            <p>{{ option.description }}</p>

            <ul class="tags">
              <li v-for="tag in option.tags" :key="tag" class="tag">
                {{ tag }}
              </li>
            </ul>

            <button class="card-button" @click="goTo(option.href)">
              {{ option.action }}
              <span aria-hidden="true">→</span>
            </button>

          </article>

        </div>

      </section>

    </main>

  </div>
</template>

<style scoped>
.app-shell {
  --bg: #171126;
  --purple: #3900A8;
  --pink: #FF4ECD;
  --mint: #00E5A8;
  --text: #F8F5FF;
  --text-secondary: #C5BBD3;

  display: flex;
  min-height: 100vh;

  background:
    radial-gradient(ellipse 700px 500px at 85% 0%, rgba(57, 0, 168, 0.55), transparent 70%),
    radial-gradient(ellipse 600px 400px at 30% 110%, rgba(255, 78, 205, 0.15), transparent 70%),
    var(--bg);

  color: var(--text);
  font-family: 'Montserrat', sans-serif;
}

.content {
  flex: 1;
  min-width: 0;

  display: flex;
  flex-direction: column;
}

/* ========================================
   TOP BAR
======================================== */

.topbar {
  height: 84px;
  padding: 0 56px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  background: rgba(23, 17, 38, 0.7);
  border-bottom: 1px solid rgba(139, 43, 255, 0.25);
}

.breadcrumb {
  flex: 1;

  color: #8E82A6;
  font-size: 14px;
  font-weight: 600;
}

.breadcrumb strong {
  color: var(--text);
}

.topbar-spacer {
  flex: 1;
}

.steps {
  display: flex;
  align-items: center;
  gap: 10px;

  list-style: none;
}

.step {
  display: flex;
  align-items: center;
  gap: 9px;

  color: #7D7096;
  font-size: 13px;
  font-weight: 700;
}

.step-dot {
  width: 26px;
  height: 26px;

  display: grid;
  place-items: center;

  border: 1.5px solid #4A3D66;
  border-radius: 50%;

  font-size: 12px;
}

.step.active {
  color: var(--text);
}

.step.active .step-dot {
  background: var(--mint);
  border-color: var(--mint);
  color: var(--bg);
}

.step-line {
  width: 34px;
  height: 1.5px;
  background: #3A2F55;
}

/* ========================================
   BODY
======================================== */

.body {
  width: 100%;
  max-width: 1300px;

  padding: 56px;
}

.eyebrow {
  display: block;
  margin-bottom: 16px;

  color: var(--pink);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 5px;
}

h1 {
  margin-bottom: 14px;

  font-size: clamp(32px, 3vw, 46px);
  font-weight: 800;
  letter-spacing: -1.2px;
}

.lead {
  max-width: 760px;
  margin-bottom: 44px;

  color: var(--text-secondary);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.5;
}

/* ========================================
   CARDS
======================================== */

.cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 28px;
}

.card {
  position: relative;

  display: flex;
  flex-direction: column;

  min-height: 430px;
  padding: 34px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.22);
  border-radius: 20px;

  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
}

.card.green {
  border-color: rgba(0, 229, 168, 0.55);
  box-shadow: 0 0 60px rgba(0, 229, 168, 0.1);
}

.card.pink {
  border-color: rgba(255, 78, 205, 0.45);
}

.recommended {
  position: absolute;
  top: -13px;
  right: 28px;

  padding: 6px 12px;

  background: var(--mint);
  border-radius: 99px;

  color: var(--bg);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
}

.badge {
  width: 62px;
  height: 62px;

  display: grid;
  place-items: center;

  margin-bottom: 24px;
  border-radius: 16px;
}

.green .badge {
  background: rgba(0, 229, 168, 0.14);
}

.pink .badge {
  background: rgba(255, 78, 205, 0.14);
}

.badge svg {
  width: 30px;
  height: 30px;

  fill: none;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.green .badge svg {
  stroke: var(--mint);
}

.pink .badge svg {
  stroke: var(--pink);
}

.card h2 {
  margin-bottom: 10px;

  font-size: 28px;
  font-weight: 800;
}

.card p {
  margin-bottom: 22px;

  color: var(--text-secondary);
  font-size: 16px;
  font-weight: 500;
  line-height: 1.55;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;

  margin-bottom: auto;
  list-style: none;
}

.tag {
  padding: 7px 13px;

  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 99px;

  color: #E2D6F5;
  font-size: 12px;
  font-weight: 700;
}

/* Buttons */

.card-button {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-top: 26px;
  padding: 17px 26px;

  border-radius: 10px;

  font-family: inherit;
  font-size: 16px;
  font-weight: 800;

  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.green .card-button {
  background: var(--mint);
  border: none;
  color: var(--bg);

  box-shadow: 0 10px 30px rgba(0, 229, 168, 0.3);
}

.pink .card-button {
  background: transparent;
  border: 1.5px solid var(--pink);
  color: var(--pink);
}

.green .card-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.pink .card-button:hover {
  background: rgba(255, 78, 205, 0.12);
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .cards {
    grid-template-columns: 1fr;
  }

  .card {
    min-height: auto;
  }

  .tags {
    margin-bottom: 0;
  }
}

@media (max-width: 900px) {
  .app-shell {
    flex-direction: column;
  }

  .topbar {
    height: auto;
    padding: 16px 5%;
  }

  .breadcrumb,
  .topbar-spacer {
    display: none;
  }

  .steps {
    width: 100%;
    justify-content: space-between;
  }

  .step:not(.active) {
    font-size: 0;
    gap: 0;
  }

  .step-line {
    flex: 1;
  }

  .body {
    padding: 40px 5%;
  }
}

@media (prefers-reduced-motion: reduce) {
  .card,
  .card-button {
    transition: none;
  }
}
</style>