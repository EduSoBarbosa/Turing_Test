<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

/* ========================================
   TIPOS
======================================== */

type Choice = 'A' | 'B'

interface JudgmentItem {
  questionId: number
  question: string
  human: string
  ai: string
  flipped: boolean // false → A é a humana | true → A é a IA
}

interface StoredJudgment {
  source: string
  items: JudgmentItem[]
  choices: Record<number, Choice>
}

interface ResultItem {
  index: number
  item: JudgmentItem
  choice: Choice | undefined
  humanLabel: Choice
  correct: boolean
}

/* ========================================
   CONFIG
======================================== */

const JUDGMENT_KEY = 'eliza:judgment'
const QUIZ_KEY = 'eliza:quiz'
const FINALIZED_KEY = 'eliza:finalized'

const LABELS: Choice[] = ['A', 'B']

const steps = ['Choose', 'Responses', 'Judgment', 'Results']
const currentStep = 3

/* ========================================
   ESTADO
======================================== */

const router = useRouter()

const status = ref<'loading' | 'ready' | 'empty'>('loading')
const stored = ref<StoredJudgment | null>(null)

const filter = ref<'all' | 'correct' | 'wrong'>('all')
const openRows = ref<number[]>([])
const animated = ref(false)

onMounted(() => {
  try {
    const finalized = sessionStorage.getItem(FINALIZED_KEY) === '1'
    const raw = sessionStorage.getItem(JUDGMENT_KEY)
    const data = raw ? (JSON.parse(raw) as StoredJudgment) : null

    if (finalized && data && data.items?.length) {
      stored.value = data
      status.value = 'ready'

      // anima o anel de pontuação depois de montar
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          animated.value = true
        })
      })

      return
    }
  } catch {
    /* cai no estado vazio */
  }

  status.value = 'empty'
})

/* ========================================
   RESULTADO
======================================== */

const results = computed<ResultItem[]>(() => {
  if (!stored.value) return []

  const { items, choices } = stored.value

  return items.map((item, index) => {
    const humanLabel: Choice = item.flipped ? 'B' : 'A'
    const choice = choices[item.questionId]

    return {
      index,
      item,
      choice,
      humanLabel,
      correct: choice === humanLabel
    }
  })
})

const total = computed(() => results.value.length)
const correctCount = computed(() => results.value.filter((r) => r.correct).length)
const wrongCount = computed(() => total.value - correctCount.value)

const percent = computed(() =>
  total.value ? Math.round((correctCount.value / total.value) * 100) : 0
)

const verdict = computed(() => {
  const p = percent.value

  if (p >= 80) {
    return {
      title: 'Keen eye',
      text: 'You identified most of the human responses. This time, the AI rarely fooled you.'
    }
  }

  if (p >= 60) {
    return {
      title: 'Good instincts',
      text: 'You got more right than wrong, though some AI responses seemed human.'
    }
  }

  if (p >= 40) {
    return {
      title: 'Close to chance',
      text: 'Your score was close to chance. It was hard to tell which responses were written by a person.'
    }
  }

  return {
    title: 'The AI fooled you',
    text: 'You picked the AI response as human more often than you picked the human response.'
  }
})

/* anel de pontuação */
const RADIUS = 78
const CIRCUMFERENCE = 2 * Math.PI * RADIUS

const ringOffset = computed(() =>
  animated.value
    ? CIRCUMFERENCE * (1 - percent.value / 100)
    : CIRCUMFERENCE
)

/* ========================================
   LISTA
======================================== */

const visible = computed(() => {
  if (filter.value === 'correct') return results.value.filter((r) => r.correct)
  if (filter.value === 'wrong') return results.value.filter((r) => !r.correct)

  return results.value
})

const filters = computed(() => [
  { id: 'all' as const, label: 'All', count: total.value },
  { id: 'correct' as const, label: 'Correct', count: correctCount.value },
  { id: 'wrong' as const, label: 'Incorrect', count: wrongCount.value }
])

const isOpen = (index: number) => openRows.value.includes(index)

function toggle(index: number) {
  openRows.value = isOpen(index)
    ? openRows.value.filter((i) => i !== index)
    : [...openRows.value, index]
}

const allOpen = computed(
  () => visible.value.length > 0 && visible.value.every((r) => isOpen(r.index))
)

function toggleAll() {
  openRows.value = allOpen.value ? [] : visible.value.map((r) => r.index)
}

const textOf = (r: ResultItem, label: Choice) => {
  const aText = r.item.flipped ? r.item.ai : r.item.human
  const bText = r.item.flipped ? r.item.human : r.item.ai

  return label === 'A' ? aText : bText
}

const originOf = (r: ResultItem, label: Choice) =>
  label === r.humanLabel ? 'human' : 'ai'

/* ========================================
   AÇÕES
======================================== */

function clearSession() {
  sessionStorage.removeItem(JUDGMENT_KEY)
  sessionStorage.removeItem(QUIZ_KEY)
  sessionStorage.removeItem(FINALIZED_KEY)
}

function newExperiment() {
  clearSession()
  router.push('/quiz')
}

function openLibrary() {
  router.push('/questionarios')
}
</script>

<template>
  <div class="result-shell">

    <!-- TOP BAR -->
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

      <span class="topbar-spacer" aria-hidden="true" />

    </header>

    <main class="stage">

      <!-- LOADING -->
      <div v-if="status === 'loading'" class="state" role="status">
        <span class="spinner" aria-hidden="true" />
        Loading results…
      </div>

      <!-- EMPTY / SEM ACESSO -->
      <div v-else-if="status === 'empty'" class="state column">
        <p>No results yet. Submit a judgment first.</p>
        <button class="outline" @click="router.push('/quiz')">
          Choose an experiment
        </button>
      </div>

      <!-- READY -->
      <template v-else>

        <span class="eyebrow">FINAL RESULTS</span>

        <!-- HERO -->
        <section class="hero">

          <div class="score" role="img" :aria-label="`${correctCount} correct out of ${total} questions`">

            <svg viewBox="0 0 180 180" aria-hidden="true">
              <defs>
                <linearGradient id="ring-gradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#FF4ECD" />
                  <stop offset="100%" stop-color="#00E5A8" />
                </linearGradient>
              </defs>

              <circle
                class="ring-track"
                cx="90"
                cy="90"
                :r="RADIUS"
              />

              <circle
                class="ring-fill"
                cx="90"
                cy="90"
                :r="RADIUS"
                :stroke-dasharray="CIRCUMFERENCE"
                :stroke-dashoffset="ringOffset"
              />
            </svg>

            <div class="score-center">
              <strong>{{ correctCount }}<small>/{{ total }}</small></strong>
              <span>{{ percent }}% correct</span>
            </div>

          </div>

          <div class="hero-text">

            <h1>{{ verdict.title }}</h1>

            <p class="verdict">{{ verdict.text }}</p>

            <ul class="chips">
              <li class="chip good">✓ {{ correctCount }} {{ correctCount === 1 ? 'correct answer' : 'correct answers' }}</li>
              <li class="chip bad">✕ {{ wrongCount }} {{ wrongCount === 1 ? 'incorrect answer' : 'incorrect answers' }}</li>
            </ul>

            <p class="note">
              With two choices per question, random guesses average about 50% correct.
            </p>

            <div class="hero-actions">
              <button class="primary" @click="newExperiment">
                Start a new experiment <span aria-hidden="true">→</span>
              </button>

              <button class="ghost" @click="openLibrary">
                Browse questionnaires
              </button>
            </div>

          </div>

        </section>

        <!-- REVIEW -->
        <section class="review">

          <div class="review-head">

            <h2>Review responses</h2>

            <div class="review-tools">

              <div class="tabs" role="tablist" aria-label="Filter questions">
                <button
                  v-for="f in filters"
                  :key="f.id"
                  class="tab"
                  :class="{ on: filter === f.id }"
                  role="tab"
                  :aria-selected="filter === f.id"
                  @click="filter = f.id"
                >
                  {{ f.label }} <span>{{ f.count }}</span>
                </button>
              </div>

              <button class="link" @click="toggleAll">
                {{ allOpen ? 'Collapse all' : 'Expand all' }}
              </button>

            </div>

          </div>

          <p v-if="visible.length === 0" class="empty-filter">
            No questions in this category.
          </p>

          <ol v-else class="rows">

            <li
              v-for="r in visible"
              :key="r.item.questionId"
              class="row"
              :class="{ wrong: !r.correct, open: isOpen(r.index) }"
            >

              <button
                class="row-head"
                :aria-expanded="isOpen(r.index)"
                @click="toggle(r.index)"
              >

                <span class="number">
                  {{ String(r.index + 1).padStart(2, '0') }}
                </span>

                <span class="row-question">{{ r.item.question }}</span>

                <span class="badge" :class="r.correct ? 'good' : 'bad'">
                  {{ r.correct ? '✓ Correct' : '✕ Incorrect' }}
                </span>

                <span class="chevron" aria-hidden="true">▾</span>

              </button>

              <div v-if="isOpen(r.index)" class="reveal">

                <div
                  v-for="label in LABELS"
                  :key="label"
                  class="ans"
                  :class="originOf(r, label)"
                >

                  <div class="ans-head">
                    <span class="ans-label">
                      RESPONSE {{ label }} ·
                      {{ originOf(r, label) === 'human' ? 'HUMAN' : 'AI' }}
                    </span>

                    <span v-if="r.choice === label" class="picked">
                      Your choice
                    </span>
                  </div>

                  <p>{{ textOf(r, label) }}</p>

                </div>

              </div>

            </li>

          </ol>

        </section>

      </template>

    </main>

  </div>
</template>

<style scoped>
.result-shell {
  --bg: #171126;
  --purple: #3900A8;
  --lavender: #C5A3FF;
  --pink: #FF4ECD;
  --mint: #00E5A8;
  --wrong: #FF8A8A;
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
  height: 84px;
  padding: 0 56px;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;

  background: rgba(18, 12, 32, 0.85);
  border-bottom: 1px solid rgba(139, 43, 255, 0.3);
}

.brand {
  flex: 1;

  display: flex;
  align-items: center;
  gap: 14px;
}

.topbar-spacer {
  flex: 1;
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
   STAGE
======================================== */

.stage {
  flex: 1;

  width: 100%;
  max-width: 1200px;
  margin: 0 auto;

  padding: 52px 56px 72px;
}

.eyebrow {
  display: block;
  margin-bottom: 24px;

  color: var(--pink);
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 5px;
}

/* ========================================
   HERO
======================================== */

.hero {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 56px;
  align-items: center;

  margin-bottom: 64px;
  padding: 44px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 229, 168, 0.4);
  border-radius: 24px;

  box-shadow: 0 0 80px rgba(0, 229, 168, 0.08);
}

.score {
  position: relative;

  width: 260px;
  height: 260px;
}

.score svg {
  width: 100%;
  height: 100%;

  transform: rotate(-90deg);
}

.score circle {
  fill: none;
  stroke-width: 12;
}

.ring-track {
  stroke: rgba(197, 163, 255, 0.15);
}

.ring-fill {
  stroke: url(#ring-gradient);
  stroke-linecap: round;

  transition: stroke-dashoffset 1.4s cubic-bezier(0.22, 1, 0.36, 1);
}

.score-center {
  position: absolute;
  inset: 0;

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.score-center strong {
  font-size: 64px;
  font-weight: 800;
  letter-spacing: -2px;
  line-height: 1;
}

.score-center small {
  color: var(--text-secondary);
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 0;
}

.score-center span {
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
}

.hero-text h1 {
  margin-bottom: 14px;

  font-size: clamp(32px, 3.4vw, 48px);
  font-weight: 800;
  letter-spacing: -1.4px;
  line-height: 1.1;
}

.verdict {
  max-width: 620px;
  margin-bottom: 22px;

  font-size: 18px;
  font-weight: 500;
  line-height: 1.55;
}

.chips {
  display: flex;
  gap: 10px;

  margin-bottom: 22px;
  list-style: none;
}

.chip {
  padding: 7px 14px;

  border-radius: 99px;

  font-size: 13px;
  font-weight: 800;
}

.chip.good {
  background: rgba(0, 229, 168, 0.14);
  color: var(--mint);
}

.chip.bad {
  background: rgba(255, 138, 138, 0.14);
  color: var(--wrong);
}

.note {
  max-width: 620px;
  margin-bottom: 30px;

  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 14px;
}

.primary,
.ghost {
  display: inline-flex;
  align-items: center;
  gap: 12px;

  padding: 16px 28px;

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

.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.ghost {
  background: transparent;
  border: 1.5px solid rgba(248, 245, 255, 0.3);
  color: var(--text);
}

.ghost:hover {
  background: rgba(255, 255, 255, 0.06);
}

/* ========================================
   REVIEW
======================================== */

.review-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;

  margin-bottom: 22px;
}

.review-head h2 {
  font-size: 24px;
  font-weight: 800;
}

.review-tools {
  display: flex;
  align-items: center;
  gap: 18px;
}

.tabs {
  display: flex;
  gap: 6px;

  padding: 4px;

  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
}

.tab {
  display: flex;
  align-items: center;
  gap: 8px;

  padding: 8px 14px;

  background: transparent;
  border: none;
  border-radius: 7px;

  color: var(--text-secondary);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;
  transition: background 0.25s ease, color 0.25s ease;
}

.tab span {
  color: #8E82A6;
  font-size: 12px;
}

.tab.on {
  background: rgba(57, 0, 168, 0.7);
  color: var(--text);
}

.tab.on span {
  color: var(--mint);
}

.link {
  padding: 0;

  background: none;
  border: none;

  color: var(--lavender);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;
}

.link:hover {
  color: var(--text);
}

.empty-filter {
  padding: 28px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.2);
  border-radius: 14px;

  color: var(--text-secondary);
  font-weight: 600;
}

.rows {
  display: flex;
  flex-direction: column;
  gap: 12px;

  list-style: none;
}

.row {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.2);
  border-radius: 14px;

  transition: border-color 0.25s ease;
}

.row.wrong {
  border-color: rgba(255, 138, 138, 0.35);
}

.row.open {
  border-color: rgba(197, 163, 255, 0.5);
}

.row-head {
  width: 100%;

  display: flex;
  align-items: center;
  gap: 18px;

  padding: 18px 22px;

  background: none;
  border: none;

  color: inherit;
  font-family: inherit;
  text-align: left;

  cursor: pointer;
}

.row-head:focus-visible {
  outline: 2px solid var(--lavender);
  outline-offset: -2px;
  border-radius: 14px;
}

.number {
  flex-shrink: 0;

  color: var(--pink);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 2px;
}

.row-question {
  flex: 1;

  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.badge {
  flex-shrink: 0;

  padding: 5px 12px;

  border-radius: 99px;

  font-size: 12px;
  font-weight: 800;
}

.badge.good {
  background: rgba(0, 229, 168, 0.14);
  color: var(--mint);
}

.badge.bad {
  background: rgba(255, 138, 138, 0.14);
  color: var(--wrong);
}

.chevron {
  flex-shrink: 0;

  color: #8E82A6;
  transition: transform 0.25s ease;
}

.row.open .chevron {
  transform: rotate(180deg);
}

/* Reveal */

.reveal {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;

  padding: 0 22px 22px;
}

.ans {
  display: flex;
  flex-direction: column;
  gap: 12px;

  padding: 18px;

  border: 1.5px solid;
  border-radius: 14px;
}

.ans.human {
  background: rgba(0, 229, 168, 0.06);
  border-color: rgba(0, 229, 168, 0.45);
}

.ans.ai {
  background: rgba(255, 78, 205, 0.06);
  border-color: rgba(255, 78, 205, 0.45);
}

.ans-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.ans-label {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2.5px;
}

.ans.human .ans-label {
  color: var(--mint);
}

.ans.ai .ans-label {
  color: var(--pink);
}

.picked {
  padding: 3px 10px;

  background: rgba(248, 245, 255, 0.12);
  border-radius: 99px;

  font-size: 11px;
  font-weight: 800;
}

.ans p {
  font-size: 15px;
  font-weight: 500;
  line-height: 1.6;
  white-space: pre-wrap;
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
   RESPONSIVE
======================================== */

@media (max-width: 1000px) {
  .topbar {
    padding: 0 32px;
  }

  .stage {
    padding: 40px 32px 56px;
  }

  .hero {
    grid-template-columns: 1fr;
    justify-items: center;
    gap: 32px;

    padding: 36px 28px;
    text-align: center;
  }

  .chips,
  .hero-actions {
    justify-content: center;
  }
}

@media (max-width: 800px) {
  .topbar {
    height: auto;
    padding: 14px 5%;

    flex-wrap: wrap;
  }

  .brand {
    flex: none;
  }

  .brand-name,
  .topbar-spacer {
    display: none;
  }

  .steps {
    order: 3;
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

  .stage {
    padding: 28px 5% 48px;
  }

  .score {
    width: 220px;
    height: 220px;
  }

  .score-center strong {
    font-size: 52px;
  }

  .review-tools {
    width: 100%;
    justify-content: space-between;
  }

  .row-head {
    flex-wrap: wrap;
    gap: 10px 14px;
    padding: 16px;
  }

  .row-question {
    flex-basis: calc(100% - 60px);
    order: 2;
  }

  .badge {
    order: 1;
    margin-left: auto;
  }

  .chevron {
    order: 3;
    margin-left: auto;
  }

  .reveal {
    grid-template-columns: 1fr;
    padding: 0 16px 16px;
  }

  .primary,
  .ghost {
    width: 100%;
    justify-content: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 0.01ms !important;
  }

  .ring-fill,
  .chevron,
  .primary {
    transition: none;
  }
}
</style>
