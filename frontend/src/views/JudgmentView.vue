<script setup lang="ts">
import { questionnaire as sampleQuestions } from '@/lib/questionnaire'
import { ref, reactive, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'

/* ========================================
   TIPOS
======================================== */

interface RawItem {
  questionId: number
  question: string
  human: string
  ai: string
}

// flipped = false → A é a humana | flipped = true → A é a IA
interface JudgmentItem extends RawItem {
  flipped: boolean
}

type Choice = 'A' | 'B'

interface StoredJudgment {
  source: string
  items: JudgmentItem[]
  choices: Record<number, Choice>
}

/* ========================================
   CONFIG
======================================== */

const JUDGMENT_KEY = 'eliza:judgment' // ordem A/B + escolhas (a tela de resultado lê daqui)
const QUIZ_KEY = 'eliza:quiz' //          respostas vindas de "New experiment"

const steps = ['Choose', 'Responses', 'Judgment', 'Results']
const currentStep = 2

/* ========================================
   API (SUBSTITUA PELA SUA CHAMADA)
======================================== */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// Usada no caminho "Ready-made questionnaires" (?questionario=ID)
async function fetchJudgmentSet(): Promise<RawItem[]> {
  await sleep(600)
  return sampleQuestions.map(({ id, text, sampleHuman, ai }) => ({
    questionId: id,
    question: text,
    human: sampleHuman,
    ai,
  }))
}

/* ========================================
   ESTADO
======================================== */

const route = useRoute()
const router = useRouter()

const status = ref<'loading' | 'ready' | 'empty' | 'error'>('loading')
const source = ref('novo')
const items = ref<JudgmentItem[]>([])
const choices = reactive<Record<number, Choice>>({})
const currentIndex = ref(0)
const showExitModal = ref(false)

/* ========================================
   ORDEM A/B (sorteada uma vez e guardada)
======================================== */

// metade das perguntas com a humana em A e metade em B, embaralhado
function assignOrder(raw: RawItem[]): JudgmentItem[] {
  const flags = raw.map((_, index) => index % 2 === 0)

  for (let i = flags.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[flags[i], flags[j]] = [flags[j], flags[i]]
  }

  return raw.map((item, index) => ({ ...item, flipped: flags[index] }))
}

function persist() {
  const data: StoredJudgment = {
    source: source.value,
    items: items.value,
    choices: { ...choices }
  }

  sessionStorage.setItem(JUDGMENT_KEY, JSON.stringify(data))
}

function readStored(): StoredJudgment | null {
  try {
    const raw = sessionStorage.getItem(JUDGMENT_KEY)
    return raw ? (JSON.parse(raw) as StoredJudgment) : null
  } catch {
    return null
  }
}

/* ========================================
   CARREGAMENTO
======================================== */

async function load() {
  status.value = 'loading'

  source.value =
    typeof route.query.questionario === 'string'
      ? route.query.questionario
      : 'novo'

  try {
    // 1) restaura se a pessoa atualizou a página no meio do julgamento
    const saved = readStored()

    if (saved && saved.source === source.value && saved.items.length) {
      items.value = saved.items
      Object.assign(choices, saved.choices)

      // ?pergunta=N (vindo de "Alterar" na tela de confirmação) abre direto nela
      const wanted = Number(route.query.pergunta)

      if (Number.isInteger(wanted) && wanted >= 1 && wanted <= items.value.length) {
        currentIndex.value = wanted - 1
      } else {
        const firstOpen = items.value.findIndex((i) => !choices[i.questionId])
        currentIndex.value = firstOpen === -1 ? items.value.length - 1 : firstOpen
      }

      status.value = 'ready'
      return
    }

    // 2) começa um julgamento novo
    let raw: RawItem[] = []

    if (source.value === 'novo') {
      const stored = sessionStorage.getItem(QUIZ_KEY)
      raw = stored ? (JSON.parse(stored) as RawItem[]) : []
    } else {
      raw = await fetchJudgmentSet()
    }

    if (!raw.length) {
      status.value = 'empty'
      return
    }

    items.value = assignOrder(raw)
    persist()

    status.value = 'ready'
  } catch {
    status.value = 'error'
  }
}

/* ========================================
   JULGAMENTO
======================================== */

const total = computed(() => items.value.length)
const current = computed(() => items.value[currentIndex.value])

const answeredCount = computed(
  () => items.value.filter((i) => choices[i.questionId]).length
)

const allAnswered = computed(
  () => total.value > 0 && answeredCount.value === total.value
)

const isLast = computed(() => currentIndex.value === total.value - 1)

const progress = computed(() =>
  total.value ? ((currentIndex.value + 1) / total.value) * 100 : 0
)

const textFor = (item: JudgmentItem, label: Choice) => {
  const aText = item.flipped ? item.ai : item.human
  const bText = item.flipped ? item.human : item.ai

  return label === 'A' ? aText : bText
}

const selected = computed(() =>
  current.value ? choices[current.value.questionId] : undefined
)

function choose(label: Choice) {
  if (!current.value) return

  choices[current.value.questionId] = label
  persist()
}

const goTo = (index: number) => {
  if (index >= 0 && index < total.value) currentIndex.value = index
}

const prev = () => goTo(currentIndex.value - 1)
const next = () => goTo(currentIndex.value + 1)

function finish() {
  if (!allAnswered.value) return

  persist()
  router.push('/quiz/finalizar')
}

function exitJudgment() {
  sessionStorage.removeItem(JUDGMENT_KEY)
  sessionStorage.removeItem(QUIZ_KEY)

  router.push('/quiz')
}

/* ========================================
   ATALHOS DE TECLADO
======================================== */

function onKeydown(event: KeyboardEvent) {
  if (status.value !== 'ready') return

  if (showExitModal.value) {
    if (event.key === 'Escape') showExitModal.value = false
    return
  }

  const key = event.key.toLowerCase()

  if (key === 'a' || key === '1') choose('A')
  else if (key === 'b' || key === '2') choose('B')
  else if (event.key === 'ArrowLeft') prev()
  else if (event.key === 'ArrowRight' && !isLast.value) next()
}

onMounted(() => {
  load()
  window.addEventListener('keydown', onKeydown)
})

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>

<template>
  <div class="judge-shell">

    <!-- TOP BAR (sem sidebar: foco total no julgamento) -->
    <header class="topbar">

      <div class="brand">
        <img
          src="../assets/eliza-logo.png"
          alt="ELIZA logo"
          class="brand-logo"
        />
        <span class="brand-name">ELIZA</span>
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

      <button class="exit" @click="showExitModal = true">
          Leave
</button>

    </header>

    <main class="stage">

      <!-- LOADING -->
      <div v-if="status === 'loading'" class="state" role="status">
        <span class="spinner" aria-hidden="true" />
        Preparing the judgment…
      </div>

      <!-- EMPTY -->
      <div v-else-if="status === 'empty'" class="state column">
        <p>No judgment is in progress.</p>
        <button class="outline" @click="router.push('/quiz')">
          Choose an experiment
        </button>
      </div>

      <!-- ERROR -->
      <div v-else-if="status === 'error'" class="state column">
        <p>Could not load the judgment.</p>
        <button class="outline" @click="load">Try again</button>
      </div>

      <!-- READY -->
      <template v-else-if="current">

        <!-- PROGRESS -->
        <div class="progress">

          <div class="progress-info">
            <span class="eyebrow">
              QUESTION {{ String(currentIndex + 1).padStart(2, '0') }}
              OF {{ String(total).padStart(2, '0') }}
            </span>
            <span class="answered">
              {{ answeredCount }}/{{ total }} judged
            </span>
          </div>

          <div
            class="bar"
            role="progressbar"
            :aria-valuenow="currentIndex + 1"
            aria-valuemin="1"
            :aria-valuemax="total"
          >
            <div class="bar-fill" :style="{ width: progress + '%' }" />
          </div>

        </div>

        <!-- QUESTION -->
        <h1>{{ current.question }}</h1>

        <p class="instruction">
          A person wrote one response and an AI generated the other.
          <strong>Which response did the person write?</strong>
        </p>

        <!-- ANSWERS -->
        <div
          class="answers"
          role="radiogroup"
          aria-label="Which response did the person write?"
        >

          <button
            v-for="label in (['A', 'B'] as const)"
            :key="`${current.questionId}-${label}`"
            class="answer"
            :class="{ selected: selected === label }"
            role="radio"
            :aria-checked="selected === label"
            @click="choose(label)"
          >

            <div class="answer-head">
              <span class="answer-label">RESPONSE {{ label }}</span>
              <kbd>{{ label }}</kbd>
            </div>

            <p class="answer-text">{{ textFor(current, label) }}</p>

            <div class="answer-foot">
              <span v-if="selected === label" class="picked">
                ✓ Selected as human
              </span>
              <span v-else class="pick-hint">
                Select as human
              </span>
            </div>

          </button>

        </div>

        <!-- QUESTION DOTS -->
        <nav class="dots" aria-label="Navigate between questions">
          <button
            v-for="(item, index) in items"
            :key="item.questionId"
            class="dot"
            :class="{
              current: index === currentIndex,
              answered: choices[item.questionId]
            }"
            :aria-label="`Go to question ${index + 1}`"
            :aria-current="index === currentIndex ? 'step' : undefined"
            @click="goTo(index)"
          >
            {{ index + 1 }}
          </button>
        </nav>

      </template>

    </main>

    <!-- ACTION BAR -->
    <footer v-if="status === 'ready'" class="action-bar">

      <button
        class="ghost"
        :disabled="currentIndex === 0"
        @click="prev"
      >
        <span aria-hidden="true">←</span> Previous
      </button>

      <div class="action-status" :class="{ ready: allAnswered }">
        <span class="status-dot" aria-hidden="true" />
        {{
          allAnswered
            ? 'All responses judged. You can finish now.'
            : `${total - answeredCount} left to judge`
        }}
      </div>

      <button
        v-if="!isLast"
        class="primary"
        @click="next"
      >
        Next <span aria-hidden="true">→</span>
      </button>

      <button
        v-else
        class="primary"
        :disabled="!allAnswered"
        :title="allAnswered ? '' : 'Judge every question to finish'"
        @click="finish"
      >
        Review and submit <span aria-hidden="true">→</span>
      </button>

    </footer>

    <!-- EXIT MODAL -->
    <div
      v-if="showExitModal"
      class="overlay"
      @click.self="showExitModal = false"
    >
      <div
        class="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="exit-title"
      >
        <h2 id="exit-title">Leave this judgment?</h2>

        <p>
          Leaving clears your progress and takes you back to the experiment selection.
        </p>

        <div class="modal-actions">
          <button class="ghost" @click="showExitModal = false">
            Keep judging
          </button>
          <button class="danger" @click="exitJudgment">
            Leave anyway
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
.judge-shell {
  --bg: #171126;
  --purple: #3900A8;
  --lavender: #C5A3FF;
  --pink: #FF4ECD;
  --mint: #00E5A8;
  --text: #F8F5FF;
  --text-secondary: #C5BBD3;

  display: flex;
  flex-direction: column;
  min-height: 100vh;

  background:
    radial-gradient(ellipse 800px 500px at 50% -10%, rgba(57, 0, 168, 0.55), transparent 70%),
    radial-gradient(ellipse 600px 400px at 85% 110%, rgba(255, 78, 205, 0.12), transparent 70%),
    var(--bg);
  background-attachment: fixed;

  color: var(--text);
  font-family: 'Montserrat', sans-serif;
}

/* ========================================
   TOP BAR
======================================== */
.topbar {
  position: relative;

  min-height: 84px;
  padding: 0 56px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  background: rgba(18, 12, 32, 0.85);
  border-bottom: 1px solid rgba(139, 43, 255, 0.3);
}

/* LOGO */

.brand {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-shrink: 0;
}

.brand-logo {
  width: 46px;
  height: 46px;
  object-fit: contain;
}

.brand-name {
  color: var(--lavender);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 6px;
}

/* STEPS */

.steps {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  display: flex;
  align-items: center;
  gap: 10px;

  margin: 0;
  padding: 0;
  list-style: none;
}

.step {
  display: flex;
  align-items: center;
  gap: 9px;

  color: #7D7096;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
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
  flex-shrink: 0;
}

/* BOTÃO SAIR */

.exit {
  margin-left: auto;
  padding: 10px 20px;

  background: transparent;
  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 8px;

  color: var(--text-secondary);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;
  transition: border-color 0.25s ease, color 0.25s ease;

  flex-shrink: 0;
}

.exit:hover {
  border-color: var(--pink);
  color: var(--pink);
}
/* ========================================
   STAGE
======================================== */

.stage {
  flex: 1;

  width: 100%;
  max-width: 1200px;
  margin: 0 auto;

  padding: 44px 56px 32px;
}

/* Progress */

.progress {
  margin-bottom: 34px;
}

.progress-info {
  display: flex;
  justify-content: space-between;

  margin-bottom: 12px;
}

.eyebrow {
  color: var(--pink);
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 4px;
}

.answered {
  color: #8E82A6;
  font-size: 13px;
  font-weight: 700;
}

.bar {
  height: 5px;

  background: rgba(197, 163, 255, 0.15);
  border-radius: 99px;

  overflow: hidden;
}

.bar-fill {
  height: 100%;

  background: linear-gradient(90deg, var(--pink), var(--mint));
  border-radius: 99px;

  transition: width 0.4s ease;
}

/* Question */

h1 {
  max-width: 900px;
  margin-bottom: 14px;

  font-size: clamp(26px, 2.6vw, 38px);
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1.25;
}

.instruction {
  max-width: 760px;
  margin-bottom: 34px;

  color: var(--text-secondary);
  font-size: 17px;
  font-weight: 500;
  line-height: 1.55;
}

.instruction strong {
  color: var(--text);
}

/* ========================================
   ANSWERS
======================================== */

.answers {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;

  margin-bottom: 34px;
}

.answer {
  display: flex;
  flex-direction: column;

  min-height: 280px;
  padding: 28px;

  background: rgba(255, 255, 255, 0.04);
  border: 1.5px solid rgba(197, 163, 255, 0.25);
  border-radius: 20px;

  color: inherit;
  font-family: inherit;
  text-align: left;

  cursor: pointer;

  transition:
    transform 0.3s ease,
    border-color 0.3s ease,
    background 0.3s ease,
    box-shadow 0.3s ease;
}

.answer:hover {
  transform: translateY(-3px);
  border-color: rgba(197, 163, 255, 0.6);
}

.answer:focus-visible {
  outline: none;
  box-shadow: 0 0 0 4px rgba(197, 163, 255, 0.25);
}

.answer.selected {
  background: rgba(0, 229, 168, 0.07);
  border-color: var(--mint);
  box-shadow: 0 0 50px rgba(0, 229, 168, 0.12);
}

.answer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 20px;
}

.answer-label {
  color: var(--lavender);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 3px;
}

.answer.selected .answer-label {
  color: var(--mint);
}

kbd {
  min-width: 28px;
  padding: 3px 8px;

  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 6px;

  color: #8E82A6;
  font-family: inherit;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
}

.answer-text {
  flex: 1;

  font-size: 18px;
  font-weight: 500;
  line-height: 1.6;
  white-space: pre-wrap;
}

.answer-foot {
  margin-top: 22px;
  padding-top: 16px;

  border-top: 1px solid rgba(197, 163, 255, 0.14);

  font-size: 13px;
  font-weight: 700;
}

.pick-hint {
  color: #8E82A6;
}

.picked {
  color: var(--mint);
}

/* ========================================
   DOTS
======================================== */

.dots {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
}

.dot {
  width: 36px;
  height: 36px;

  background: transparent;
  border: 1.5px solid #4A3D66;
  border-radius: 50%;

  color: #8E82A6;
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;
  transition: all 0.25s ease;
}

.dot:hover {
  border-color: var(--lavender);
  color: var(--text);
}

.dot.answered {
  background: rgba(0, 229, 168, 0.14);
  border-color: rgba(0, 229, 168, 0.6);
  color: var(--mint);
}

.dot.current {
  border-color: var(--text);
  color: var(--text);
  box-shadow: 0 0 0 3px rgba(248, 245, 255, 0.15);
}

.dot.current.answered {
  color: var(--mint);
  border-color: var(--mint);
  box-shadow: 0 0 0 3px rgba(0, 229, 168, 0.2);
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
  text-align: center;
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

.primary,
.ghost,
.danger {
  display: inline-flex;
  align-items: center;
  gap: 12px;

  padding: 15px 28px;

  border-radius: 10px;

  font-family: inherit;
  font-size: 15px;
  font-weight: 800;

  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, background 0.25s ease;
}

.primary {
  background: var(--mint);
  border: none;
  color: var(--bg);

  box-shadow: 0 10px 30px rgba(0, 229, 168, 0.3);
}

.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.ghost {
  background: transparent;
  border: 1.5px solid rgba(248, 245, 255, 0.3);
  color: var(--text);
}

.ghost:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.06);
}

.primary:disabled,
.ghost:disabled {
  background: rgba(255, 255, 255, 0.06);
  border-color: transparent;
  color: #7D7096;

  box-shadow: none;
  cursor: not-allowed;
}

.danger {
  background: var(--pink);
  border: none;
  color: var(--bg);
}

.danger:hover {
  transform: translateY(-2px);
}

/* ========================================
   STATES
======================================== */

.state {
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

.state.column {
  flex-direction: column;
  align-items: flex-start;
}

.spinner {
  width: 20px;
  height: 20px;

  border: 2.5px solid rgba(197, 163, 255, 0.25);
  border-top-color: var(--mint);
  border-radius: 50%;

  animation: spin 0.9s linear infinite;
}

.outline {
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

.outline:hover {
  background: rgba(255, 78, 205, 0.12);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* ========================================
   MODAL
======================================== */

.overlay {
  position: fixed;
  inset: 0;
  z-index: 100;

  display: grid;
  place-items: center;

  padding: 24px;

  background: rgba(10, 6, 20, 0.75);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.modal {
  width: 100%;
  max-width: 460px;

  padding: 32px;

  background: #1d1533;
  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 20px;
}

.modal h2 {
  margin-bottom: 12px;

  font-size: 22px;
  font-weight: 800;
}

.modal p {
  margin-bottom: 26px;

  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.55;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1000px) {
  .topbar {
    padding: 0 32px;
  }

  .stage {
    padding: 36px 32px 28px;
  }

  .action-bar {
    padding: 16px 32px;
  }
}

@media (max-width: 800px) {
  .topbar {
    height: auto;
    padding: 14px 5%;

    flex-wrap: wrap;
  }

  .brand {
    flex: 1;
  }

  .brand-name {
    display: none;
  }

  .steps {
    position: static;
    transform: none;

    order: 3;
    width: 100%;

    justify-content: space-between;
    gap: 6px;
  }

  .step:not(.active) {
    font-size: 0;
    gap: 0;
  }

  .step-line {
    flex: 1;
    width: auto;
  }

  .exit {
    margin-left: auto;
  }

  .stage {
    padding: 28px 5% 24px;
  }

  .answers {
    grid-template-columns: 1fr;
    gap: 14px;
  }

  .answer {
    min-height: 0;
    padding: 22px;
  }

  kbd {
    display: none;
  }

  .action-bar {
    flex-wrap: wrap;
    padding: 14px 5%;
  }

  .action-status {
    order: -1;
    width: 100%;
    justify-content: center;
  }

  .primary,
  .ghost {
    flex: 1;
    justify-content: center;
    padding: 14px 16px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 0.01ms !important;
  }

  .answer,
  .bar-fill,
  .primary,
  .danger {
    transition: none;
  }
}
</style>