<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'

/* ========================================
   TIPOS
======================================== */

interface Question {
  id: number
  text: string
}

type AiStatus = 'loading' | 'done' | 'error'

interface AiAnswer {
  status: AiStatus
  text: string
}

/* ========================================
   CONFIG
======================================== */

// mínimo de caracteres para considerar a resposta humana "terminada"
const MIN_CHARS = 10

// false = mostra só "Resposta pronta" e esconde o texto da IA
// (evita que a pessoa seja influenciada pela resposta da IA enquanto escreve)
const SHOW_AI_TEXT = true

const steps = ['Escolha', 'Respostas', 'Julgamento', 'Resultado']
const currentStep = 1

/* ========================================
   API (SUBSTITUA PELAS SUAS CHAMADAS)
======================================== */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

async function fetchQuestions(): Promise<Question[]> {
  // TODO: troque pela sua API
  // const res = await fetch('/api/questions')
  // return await res.json()

  await sleep(600)

  return [
    { id: 1, text: 'Qual é uma lembrança da sua infância que você nunca esqueceu?' },
    { id: 2, text: 'Como você reage quando alguém discorda de você?' },
    { id: 3, text: 'Descreva um dia em que você ficou muito frustrado(a).' },
    { id: 4, text: 'O que te faz sentir mais em paz?' },
    { id: 5, text: 'Qual foi a última vez que você mudou de opinião sobre algo importante?' },
    { id: 6, text: 'Qual é o seu maior medo e por quê?' },
    { id: 7, text: 'Conte sobre uma pessoa que marcou a sua vida.' },
    { id: 8, text: 'O que você faria se tivesse um dia livre sem nenhuma obrigação?' },
    { id: 9, text: 'Qual foi o melhor conselho que você já recebeu?' },
    { id: 10, text: 'Como você imagina a sua vida daqui a dez anos?' }
  ]
}

async function fetchAiAnswer(question: Question): Promise<string> {
  // TODO: troque pela sua API
  // const res = await fetch('/api/ai-answer', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify({ questionId: question.id })
  // })
  // const data = await res.json()
  // return data.answer

  await sleep(2000 + Math.random() * 5000)

  return `Resposta simulada da IA para: "${question.text}"`
}

/* ========================================
   ESTADO
======================================== */

const router = useRouter()

const pageStatus = ref<'loading' | 'ready' | 'error'>('loading')
const questions = ref<Question[]>([])

// respostas humanas e da IA indexadas pelo id da pergunta
const humanAnswers = reactive<Record<number, string>>({})
const aiAnswers = reactive<Record<number, AiAnswer>>({})

async function requestAi(question: Question) {
  aiAnswers[question.id] = { status: 'loading', text: '' }

  try {
    const text = await fetchAiAnswer(question)
    aiAnswers[question.id] = { status: 'done', text }
  } catch {
    aiAnswers[question.id] = { status: 'error', text: '' }
  }
}

async function init() {
  pageStatus.value = 'loading'

  try {
    questions.value = await fetchQuestions()
  } catch {
    pageStatus.value = 'error'
    return
  }

  questions.value.forEach((q) => {
    humanAnswers[q.id] = ''
  })

  pageStatus.value = 'ready'

  // a IA começa a responder todas as perguntas ao mesmo tempo
  questions.value.forEach((q) => requestAi(q))
}

onMounted(init)

/* ========================================
   PROGRESSO
======================================== */

const total = computed(() => questions.value.length)

const isHumanDone = (id: number) =>
  (humanAnswers[id] ?? '').trim().length >= MIN_CHARS

const humanDoneCount = computed(
  () => questions.value.filter((q) => isHumanDone(q.id)).length
)

const aiDoneCount = computed(
  () => questions.value.filter((q) => aiAnswers[q.id]?.status === 'done').length
)

const aiErrorCount = computed(
  () => questions.value.filter((q) => aiAnswers[q.id]?.status === 'error').length
)

const aiPendingCount = computed(
  () => questions.value.filter((q) => aiAnswers[q.id]?.status === 'loading').length
)

// só libera quando humano E IA terminaram tudo
const canContinue = computed(
  () =>
    total.value > 0 &&
    humanDoneCount.value === total.value &&
    aiDoneCount.value === total.value
)

const plural = (n: number, one: string, many: string) => (n === 1 ? one : many)

const statusMessage = computed(() => {
  if (canContinue.value) return 'Tudo pronto! Você já pode continuar.'

  const parts: string[] = []

  const missing = total.value - humanDoneCount.value
  if (missing > 0) {
    parts.push(
      `Faltam ${missing} ${plural(missing, 'resposta sua', 'respostas suas')}`
    )
  }

  if (aiPendingCount.value > 0) {
    parts.push(`IA respondendo ${aiPendingCount.value} ${plural(aiPendingCount.value, 'pergunta', 'perguntas')}`)
  }

  if (aiErrorCount.value > 0) {
    parts.push(`${aiErrorCount.value} ${plural(aiErrorCount.value, 'erro', 'erros')} na IA`)
  }

  return parts.join(' · ')
})

/* ========================================
   CONTINUAR
======================================== */

function goNext() {
  if (!canContinue.value) return

  // guarda tudo para as próximas telas (troque por Pinia/API se preferir)
  const payload = questions.value.map((q) => ({
    questionId: q.id,
    question: q.text,
    human: humanAnswers[q.id].trim(),
    ai: aiAnswers[q.id].text
  }))

  sessionStorage.setItem('eliza:quiz', JSON.stringify(payload))

  // começa um julgamento limpo (descarta ordem A/B e escolhas antigas)
  sessionStorage.removeItem('eliza:judgment')

  router.push('/quiz/julgamento')
}
</script>

<template>
  <div class="app-shell">

    <AppSidebar active="novo" />

    <main class="content">

      <!-- TOP BAR -->
      <header class="topbar">

        <div class="breadcrumb">
          Experimento / Novo / <strong>Respostas</strong>
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

        <span class="eyebrow">PASSO 2 DE 4</span>

        <h1>Responda às perguntas</h1>

        <p class="lead">
          Escreva suas respostas à esquerda. A IA responde às mesmas
          perguntas à direita, ao mesmo tempo.
        </p>

        <!-- LOADING / ERROR DA PÁGINA -->
        <div v-if="pageStatus === 'loading'" class="page-state">
          <span class="spinner" aria-hidden="true" />
          Carregando perguntas…
        </div>

        <div v-else-if="pageStatus === 'error'" class="page-state">
          Não foi possível carregar as perguntas.
          <button class="retry" @click="init">Tentar novamente</button>
        </div>

        <template v-else>

          <!-- COLUMN HEADER -->
          <div class="columns-head">

            <div class="col-chip human">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="12" cy="8" r="4" />
                <path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7" />
              </svg>
              <span>VOCÊ · HUMANO</span>
              <b>{{ humanDoneCount }}/{{ total }}</b>
            </div>

            <div class="col-chip ai">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect x="5" y="7" width="14" height="12" rx="3" />
                <path d="M12 3v4M9 13h.01M15 13h.01M9 16h6" />
              </svg>
              <span>INTELIGÊNCIA ARTIFICIAL</span>
              <b>{{ aiDoneCount }}/{{ total }}</b>
            </div>

          </div>

          <!-- QUESTIONS -->
          <article
            v-for="(q, index) in questions"
            :key="q.id"
            class="question"
          >

            <header class="question-head">
              <span class="question-number">
                PERGUNTA {{ String(index + 1).padStart(2, '0') }}
              </span>
              <h2>{{ q.text }}</h2>
            </header>

            <div class="pair">

              <!-- HUMAN -->
              <div class="cell human" :class="{ complete: isHumanDone(q.id) }">

                <textarea
                  v-model="humanAnswers[q.id]"
                  :aria-label="`Sua resposta para: ${q.text}`"
                  placeholder="Escreva sua resposta com suas próprias palavras…"
                  rows="5"
                />

                <div class="cell-foot">
                  <span class="counter">
                    {{ humanAnswers[q.id].trim().length }} caracteres
                    <template v-if="!isHumanDone(q.id)">
                      · mín. {{ MIN_CHARS }}
                    </template>
                  </span>

                  <span v-if="isHumanDone(q.id)" class="done-tag green">
                    ✓ Respondida
                  </span>
                </div>

              </div>

              <!-- AI -->
              <div
                class="cell ai"
                :class="aiAnswers[q.id]?.status"
              >

                <!-- loading -->
                <div
                  v-if="aiAnswers[q.id]?.status === 'loading'"
                  class="ai-loading"
                  role="status"
                  aria-live="polite"
                >
                  <div class="skeleton" style="width: 92%" />
                  <div class="skeleton" style="width: 78%" />
                  <div class="skeleton" style="width: 60%" />

                  <span class="ai-hint">
                    <span class="dots" aria-hidden="true"><i /><i /><i /></span>
                    IA está respondendo…
                  </span>
                </div>

                <!-- error -->
                <div
                  v-else-if="aiAnswers[q.id]?.status === 'error'"
                  class="ai-error"
                >
                  <p>Não foi possível obter a resposta da IA.</p>
                  <button class="retry" @click="requestAi(q)">
                    Tentar novamente
                  </button>
                </div>

                <!-- done -->
                <div v-else class="ai-done">
                  <p v-if="SHOW_AI_TEXT" class="ai-text">
                    {{ aiAnswers[q.id]?.text }}
                  </p>
                  <p v-else class="ai-text muted">
                    A IA já respondeu esta pergunta.
                  </p>

                  <div class="cell-foot">
                    <span />
                    <span class="done-tag pink">✓ Respondida</span>
                  </div>
                </div>

              </div>

            </div>

          </article>

        </template>

      </section>

      <!-- FOOTER -->
      <footer v-if="pageStatus === 'ready'" class="action-bar">

        <div class="action-status" :class="{ ready: canContinue }">
          <span class="status-dot" aria-hidden="true" />
          {{ statusMessage }}
        </div>

        <button
          class="continue-button"
          :disabled="!canContinue"
          :title="canContinue ? '' : 'Disponível quando você e a IA terminarem todas as respostas'"
          @click="goNext"
        >
          Continuar
          <span aria-hidden="true">→</span>
        </button>

      </footer>

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

  padding: 56px 56px 40px;
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
  margin-bottom: 36px;

  color: var(--text-secondary);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.5;
}

/* Page states */

.page-state {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 28px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.22);
  border-radius: 16px;

  color: var(--text-secondary);
  font-weight: 600;
}

.spinner {
  width: 20px;
  height: 20px;

  border: 2.5px solid rgba(197, 163, 255, 0.25);
  border-top-color: var(--mint);
  border-radius: 50%;

  animation: spin 0.9s linear infinite;
}

/* ========================================
   COLUMNS HEADER
======================================== */

.columns-head {
  position: sticky;
  top: 0;
  z-index: 5;

  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;

  padding: 14px 0;
  margin-bottom: 10px;

  background: rgba(23, 17, 38, 0.92);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.col-chip {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 12px 18px;

  border-radius: 12px;
  border: 1px solid;

  font-size: 12px;
  font-weight: 800;
  letter-spacing: 3px;
}

.col-chip svg {
  width: 20px;
  height: 20px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.col-chip b {
  margin-left: auto;
  letter-spacing: 1px;
  font-size: 13px;
}

.col-chip.human {
  color: var(--mint);
  border-color: rgba(0, 229, 168, 0.4);
  background: rgba(0, 229, 168, 0.07);
}

.col-chip.ai {
  color: var(--pink);
  border-color: rgba(255, 78, 205, 0.4);
  background: rgba(255, 78, 205, 0.07);
}

/* ========================================
   QUESTIONS
======================================== */

.question {
  margin-bottom: 34px;
}

.question-head {
  margin-bottom: 14px;
}

.question-number {
  display: block;
  margin-bottom: 6px;

  color: #8E82A6;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 3px;
}

.question-head h2 {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.35;
}

.pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.cell {
  display: flex;
  flex-direction: column;

  min-height: 170px;
  padding: 18px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.2);
  border-radius: 16px;

  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.cell.human:focus-within {
  border-color: var(--mint);
  box-shadow: 0 0 0 4px rgba(0, 229, 168, 0.12);
}

.cell.human.complete {
  border-color: rgba(0, 229, 168, 0.45);
}

.cell.ai.done {
  border-color: rgba(255, 78, 205, 0.4);
}

.cell.ai.error {
  border-color: rgba(255, 110, 110, 0.5);
}

/* Human textarea */

textarea {
  flex: 1;

  width: 100%;
  min-height: 105px;

  background: transparent;
  border: none;
  outline: none;
  resize: vertical;

  color: var(--text);
  font-family: inherit;
  font-size: 16px;
  font-weight: 500;
  line-height: 1.55;
}

textarea::placeholder {
  color: #7D7096;
}

.cell-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-top: 12px;
  padding-top: 12px;

  border-top: 1px solid rgba(197, 163, 255, 0.12);
}

.counter {
  color: #8E82A6;
  font-size: 12px;
  font-weight: 600;
}

.done-tag {
  padding: 5px 11px;
  border-radius: 99px;

  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1px;
}

.done-tag.green {
  background: rgba(0, 229, 168, 0.14);
  color: var(--mint);
}

.done-tag.pink {
  background: rgba(255, 78, 205, 0.14);
  color: var(--pink);
}

/* AI states */

.ai-loading,
.ai-done,
.ai-error {
  flex: 1;

  display: flex;
  flex-direction: column;
}

.ai-loading {
  gap: 12px;
}

.skeleton {
  height: 14px;
  border-radius: 99px;

  background: linear-gradient(
    90deg,
    rgba(197, 163, 255, 0.08) 0%,
    rgba(197, 163, 255, 0.22) 50%,
    rgba(197, 163, 255, 0.08) 100%
  );
  background-size: 200% 100%;

  animation: shimmer 1.6s ease-in-out infinite;
}

.ai-hint {
  display: flex;
  align-items: center;
  gap: 10px;

  margin-top: auto;

  color: var(--pink);
  font-size: 13px;
  font-weight: 700;
}

.dots {
  display: inline-flex;
  gap: 4px;
}

.dots i {
  width: 6px;
  height: 6px;

  background: var(--pink);
  border-radius: 50%;

  animation: bounce 1.2s ease-in-out infinite;
}

.dots i:nth-child(2) { animation-delay: 0.15s; }
.dots i:nth-child(3) { animation-delay: 0.3s; }

.ai-text {
  flex: 1;

  font-size: 16px;
  font-weight: 500;
  line-height: 1.55;
  white-space: pre-wrap;
}

.ai-text.muted {
  color: var(--text-secondary);
}

.ai-error {
  align-items: flex-start;
  justify-content: center;
  gap: 14px;

  color: #FF9B9B;
  font-weight: 600;
}

.retry {
  padding: 10px 18px;

  background: transparent;
  border: 1.5px solid var(--pink);
  border-radius: 8px;

  color: var(--pink);
  font-family: inherit;
  font-size: 13px;
  font-weight: 800;

  cursor: pointer;
  transition: background 0.25s ease;
}

.retry:hover {
  background: rgba(255, 78, 205, 0.12);
}

/* ========================================
   ACTION BAR
======================================== */

.action-bar {
  position: sticky;
  bottom: 0;
  z-index: 10;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;

  margin-top: auto;
  padding: 18px 56px;

  background: rgba(18, 12, 32, 0.94);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);

  border-top: 1px solid rgba(139, 43, 255, 0.35);
}

.action-status {
  display: flex;
  align-items: center;
  gap: 12px;

  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.status-dot {
  width: 9px;
  height: 9px;

  background: var(--pink);
  border-radius: 50%;
  flex-shrink: 0;
}

.action-status.ready {
  color: var(--text);
}

.action-status.ready .status-dot {
  background: var(--mint);
  box-shadow: 0 0 12px var(--mint);
}

.continue-button {
  display: inline-flex;
  align-items: center;
  gap: 14px;

  padding: 16px 32px;

  background: var(--mint);
  border: none;
  border-radius: 10px;

  color: var(--bg);
  font-family: inherit;
  font-size: 16px;
  font-weight: 800;

  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0, 229, 168, 0.3);

  transition: transform 0.3s ease, box-shadow 0.3s ease, opacity 0.3s ease;
}

.continue-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.continue-button:disabled {
  background: rgba(255, 255, 255, 0.08);
  color: #7D7096;

  box-shadow: none;
  cursor: not-allowed;
}

/* ========================================
   ANIMATIONS
======================================== */

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.5; }
  40%           { transform: translateY(-5px); opacity: 1; }
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .body {
    padding: 40px 32px;
  }

  .action-bar {
    padding: 16px 32px;
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
    padding: 32px 5%;
  }

  .columns-head {
    grid-template-columns: 1fr;
    gap: 8px;
    position: static;
  }

  .pair {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .action-bar {
    flex-direction: column;
    align-items: stretch;
    padding: 14px 5%;
  }

  .continue-button {
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton,
  .dots i,
  .spinner {
    animation-duration: 0.01ms !important;
  }

  .continue-button {
    transition: none;
  }
}
</style>