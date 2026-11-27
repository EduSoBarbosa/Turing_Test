<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'

/* ========================================
   CONFIG
======================================== */

const QUESTION_COUNT = 10
const ESTIMATED_TIME = '~10 min'

const steps = ['Escolha', 'Respostas', 'Julgamento', 'Resultado']
const currentStep = 1

const howItWorks = [
  {
    title: 'Você responde',
    text: `Escreva com suas próprias palavras as respostas para ${QUESTION_COUNT} perguntas sobre experiências, opiniões e emoções.`
  },
  {
    title: 'A IA responde também',
    text: 'Enquanto você escreve, uma inteligência artificial responde às mesmas perguntas, ao mesmo tempo.'
  },
  {
    title: 'Você julga',
    text: 'Para cada pergunta, você verá duas respostas embaralhadas e vai apontar qual foi escrita por um humano.'
  },
  {
    title: 'Você vê o resultado',
    text: 'No final, descobre seus acertos e erros e quais respostas eram de quem.'
  }
]

const tips = [
  'Não existe resposta certa ou errada. Escreva do seu jeito.',
  'Não copie de outras fontes nem use outra IA. Isso estraga o experimento.',
  'Cada resposta precisa ter pelo menos 10 caracteres.',
  'Você só avança quando você e a IA terminarem todas as perguntas.'
]

/* ========================================
   AÇÕES
======================================== */

const router = useRouter()

// começa do zero: descarta qualquer experimento anterior da sessão
function start() {
  sessionStorage.removeItem('eliza:quiz')
  sessionStorage.removeItem('eliza:judgment')
  sessionStorage.removeItem('eliza:finalized')

  router.push('/quiz/novo/perguntas')
}
</script>

<template>
  <div class="app-shell">

    <AppSidebar active="novo" />

    <main class="content">

      <!-- TOP BAR -->
      <header class="topbar">

        <div class="breadcrumb">
          Experimento / Novo / <strong>Instruções</strong>
        </div>

        <ol class="steps">
          <template v-for="(step, index) in steps" :key="step">
            <li
              class="step"
              :class="{ active: index === currentStep, done: index < currentStep }"
            >
              <span class="step-dot">{{ index < currentStep ? '✓' : index + 1 }}</span>
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

        <span class="eyebrow">NOVO EXPERIMENTO</span>

        <h1>Antes de começar</h1>

        <p class="lead">
          Você será o avaliador deste experimento. Entenda como funciona
          e depois comece a responder.
        </p>

        <div class="layout">

          <div class="main-col">

            <!-- HOW IT WORKS -->
            <h2 class="section-title">Como funciona</h2>

            <ol class="how">
              <li
                v-for="(step, index) in howItWorks"
                :key="step.title"
                class="how-item"
              >
                <span class="how-number">{{ index + 1 }}</span>

                <div>
                  <h3>{{ step.title }}</h3>
                  <p>{{ step.text }}</p>
                </div>
              </li>
            </ol>

            <!-- TIPS -->
            <div class="tips">

              <h2 class="section-title">Para o experimento funcionar</h2>

              <ul>
                <li v-for="tip in tips" :key="tip">
                  <span class="tip-icon" aria-hidden="true">✓</span>
                  {{ tip }}
                </li>
              </ul>

            </div>

          </div>

          <!-- SUMMARY -->
          <aside class="summary">

            <h3>Resumo</h3>

            <dl>
              <div>
                <dt>Perguntas</dt>
                <dd>{{ QUESTION_COUNT }}</dd>
              </div>
              <div>
                <dt>Tempo estimado</dt>
                <dd>{{ ESTIMATED_TIME }}</dd>
              </div>
              <div>
                <dt>Participantes</dt>
                <dd>Você + IA</dd>
              </div>
            </dl>

            <button class="cta" @click="start">
              Começar a responder
              <span aria-hidden="true">→</span>
            </button>

            <button class="ghost" @click="router.push('/quiz')">
              <span aria-hidden="true">←</span> Voltar
            </button>

          </aside>

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
  background-attachment: fixed;

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

.step.done {
  color: var(--text-secondary);
}

.step.done .step-dot {
  border-color: var(--mint);
  color: var(--mint);
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

  padding: 56px 56px 64px;
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
  max-width: 720px;
  margin-bottom: 44px;

  color: var(--text-secondary);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.5;
}

.layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: 40px;

  align-items: start;
}

.section-title {
  margin-bottom: 18px;

  font-size: 20px;
  font-weight: 800;
}

/* ========================================
   HOW IT WORKS
======================================== */

.how {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;

  margin-bottom: 40px;
  list-style: none;
}

.how-item {
  display: flex;
  gap: 18px;

  padding: 24px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.22);
  border-radius: 16px;
}

.how-number {
  flex-shrink: 0;

  width: 40px;
  height: 40px;

  display: grid;
  place-items: center;

  background: rgba(255, 78, 205, 0.14);
  border-radius: 12px;

  color: var(--pink);
  font-size: 17px;
  font-weight: 800;
}

.how-item h3 {
  margin-bottom: 8px;

  font-size: 17px;
  font-weight: 800;
}

.how-item p {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.55;
}

/* ========================================
   TIPS
======================================== */

.tips ul {
  display: flex;
  flex-direction: column;
  gap: 12px;

  padding: 24px;

  background: rgba(0, 229, 168, 0.05);
  border: 1px solid rgba(0, 229, 168, 0.35);
  border-radius: 16px;

  list-style: none;
}

.tips li {
  display: flex;
  align-items: flex-start;
  gap: 14px;

  font-size: 15px;
  font-weight: 600;
  line-height: 1.5;
}

.tip-icon {
  flex-shrink: 0;

  width: 22px;
  height: 22px;

  display: grid;
  place-items: center;

  background: rgba(0, 229, 168, 0.18);
  border-radius: 50%;

  color: var(--mint);
  font-size: 12px;
  font-weight: 800;
}

/* ========================================
   SUMMARY
======================================== */

.summary {
  position: sticky;
  top: 24px;

  display: flex;
  flex-direction: column;
  gap: 22px;

  padding: 28px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 229, 168, 0.45);
  border-radius: 20px;

  box-shadow: 0 0 60px rgba(0, 229, 168, 0.08);
}

.summary h3 {
  font-size: 20px;
  font-weight: 800;
}

dl {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

dl div {
  display: flex;
  justify-content: space-between;
  gap: 16px;

  padding-bottom: 14px;
  border-bottom: 1px solid rgba(197, 163, 255, 0.12);
}

dt {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
}

dd {
  font-size: 14px;
  font-weight: 700;
  text-align: right;
}

.cta,
.ghost {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 17px 26px;

  border-radius: 10px;

  font-family: inherit;
  font-size: 16px;
  font-weight: 800;

  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.25s ease;
}

.cta {
  background: var(--mint);
  border: none;
  color: var(--bg);

  box-shadow: 0 10px 30px rgba(0, 229, 168, 0.3);
}

.cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.ghost {
  justify-content: center;
  gap: 10px;

  padding: 14px 26px;

  background: transparent;
  border: 1.5px solid rgba(248, 245, 255, 0.3);
  color: var(--text);

  font-size: 15px;
}

.ghost:hover {
  background: rgba(255, 255, 255, 0.06);
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }

  /* resumo com o botão sobe para antes do conteúdo */
  .summary {
    position: static;
    order: -1;
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
    padding: 36px 5% 48px;
  }

  .how {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .cta,
  .ghost {
    transition: none;
  }
}
</style>
