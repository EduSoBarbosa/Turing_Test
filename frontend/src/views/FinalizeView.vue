<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'

/* ========================================
   TIPOS
======================================== */

interface JudgmentItem {
  questionId: number
  question: string
  human: string
  ai: string
  flipped: boolean // false → A é a humana | true → A é a IA
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

const JUDGMENT_KEY = 'eliza:judgment'
const FINALIZED_KEY = 'eliza:finalized'

const steps = ['Choose', 'Responses', 'Judgment', 'Results']
const currentStep = 2

/* ========================================
   API (SUBSTITUA PELA SUA CHAMADA)
======================================== */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// Envia as escolhas para o back (opcional: pode calcular o resultado só no front)
async function submitJudgment(payload: {
  source: string
  answers: { questionId: number; choice: Choice }[]
}): Promise<void> {
  // TODO: troque pela sua API
  // const res = await fetch('/api/judgments', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(payload)
  // })
  // if (!res.ok) throw new Error('Falha ao enviar')

  void payload
  await sleep(800)
}

/* ========================================
   ESTADO
======================================== */

const router = useRouter()

const status = ref<'loading' | 'ready' | 'empty'>('loading')
const stored = ref<StoredJudgment | null>(null)

const submitting = ref(false)
const submitError = ref(false)

onMounted(() => {
  try {
    const raw = sessionStorage.getItem(JUDGMENT_KEY)
    const data = raw ? (JSON.parse(raw) as StoredJudgment) : null

    if (data && data.items?.length) {
      stored.value = data
      status.value = 'ready'
      return
    }
  } catch {
    /* cai no estado vazio */
  }

  status.value = 'empty'
})

/* ========================================
   DADOS DERIVADOS
======================================== */

const items = computed(() => stored.value?.items ?? [])
const choices = computed(() => stored.value?.choices ?? {})

const total = computed(() => items.value.length)

const answeredCount = computed(
  () => items.value.filter((i) => choices.value[i.questionId]).length
)

const missingCount = computed(() => total.value - answeredCount.value)

const isComplete = computed(() => total.value > 0 && missingCount.value === 0)

// texto da resposta que a pessoa marcou como "humana"
const pickedText = (item: JudgmentItem) => {
  const choice = choices.value[item.questionId]

  if (!choice) return ''

  const aText = item.flipped ? item.ai : item.human
  const bText = item.flipped ? item.human : item.ai

  return choice === 'A' ? aText : bText
}

/* ========================================
   AÇÕES
======================================== */

// volta ao julgamento (opcionalmente já na pergunta escolhida)
function backToJudgment(index?: number) {
  const query: Record<string, string> = {}

  if (stored.value && stored.value.source !== 'novo') {
    query.questionario = stored.value.source
  }

  if (index !== undefined) {
    query.pergunta = String(index + 1)
  }

  router.push({ path: '/quiz/julgamento', query })
}

async function finalize() {
  if (!stored.value || !isComplete.value || submitting.value) return

  submitting.value = true
  submitError.value = false

  try {
    await submitJudgment({
      source: stored.value.source,
      answers: items.value.map((i) => ({
        questionId: i.questionId,
        choice: choices.value[i.questionId]
      }))
    })

    // libera a tela de resultado
    sessionStorage.setItem(FINALIZED_KEY, '1')

    // replace: o botão Voltar não deve reabrir a confirmação
    router.replace('/quiz/resultado')
  } catch {
    submitError.value = true
    submitting.value = false
  }
}
</script>

<template>
  <div class="finalize-shell">

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
        Loading…
      </div>

      <!-- EMPTY -->
      <div v-else-if="status === 'empty'" class="state column">
        <p>There is no judgment to submit.</p>
        <button class="outline" @click="router.push('/quiz')">
          Choose an experiment
        </button>
      </div>

      <!-- READY -->
      <template v-else>

        <span class="eyebrow">CONFIRMATION</span>

        <h1>Review before submitting</h1>

        <p class="lead">
          Review which response you marked as human for each question. Your choices are final once submitted.
        </p>

        <div class="layout">

          <!-- REVIEW LIST -->
          <ol class="review">

            <li
              v-for="(item, index) in items"
              :key="item.questionId"
              class="row"
              :class="{ missing: !choices[item.questionId] }"
            >

              <span class="number">
                {{ String(index + 1).padStart(2, '0') }}
              </span>

              <div class="row-body">

                <h2>{{ item.question }}</h2>

                <template v-if="choices[item.questionId]">
                  <span class="picked">
                    ✓ Human: Response {{ choices[item.questionId] }}
                  </span>

                  <p class="preview">{{ pickedText(item) }}</p>
                </template>

                <span v-else class="unanswered">
                  Not judged
                </span>

              </div>

              <button
                class="edit"
                :class="{ urgent: !choices[item.questionId] }"
                @click="backToJudgment(index)"
              >
                {{ choices[item.questionId] ? 'Change' : 'Judge' }}
              </button>

            </li>

          </ol>

          <!-- SUMMARY -->
          <aside class="summary">

            <h3>Summary</h3>

            <div class="meter">
              <div class="meter-numbers">
                <strong>{{ answeredCount }}</strong>
                <span>of {{ total }} judged</span>
              </div>

              <div class="bar">
                <div
                  class="bar-fill"
                  :style="{ width: (total ? (answeredCount / total) * 100 : 0) + '%' }"
                />
              </div>
            </div>

            <div v-if="isComplete" class="notice warning">
              <b>Final submission</b>
              <span>
                Submitting locks in your choices.
              </span>
            </div>

            <div v-else class="notice missing-notice">
              <b>
                {{ missingCount }}
                {{ missingCount === 1 ? 'question still to judge' : 'questions still to judge' }}
              </b>
              <span>
                Go back and judge every question before submitting.
              </span>
            </div>

            <p v-if="submitError" class="error" role="alert">
              Could not submit your choices. Please try again.
            </p>

            <button
              class="primary"
              :disabled="!isComplete || submitting"
              @click="finalize"
            >
              <template v-if="submitting">
                <span class="spinner small" aria-hidden="true" />
                Submitting…
              </template>
              <template v-else>
                Submit and see results
                <span aria-hidden="true">→</span>
              </template>
            </button>

            <button
              class="ghost"
              :disabled="submitting"
              @click="backToJudgment()"
            >
              <span aria-hidden="true">←</span> Back to judging
            </button>

          </aside>

        </div>

      </template>

    </main>

  </div>
</template>

<style scoped>
.finalize-shell {
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

  padding: 52px 56px 64px;
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

  font-size: clamp(30px, 3vw, 44px);
  font-weight: 800;
  letter-spacing: -1.2px;
}

.lead {
  max-width: 720px;
  margin-bottom: 40px;

  color: var(--text-secondary);
  font-size: 17px;
  font-weight: 500;
  line-height: 1.6;
}

.layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 40px;

  align-items: start;
}

/* ========================================
   REVIEW LIST
======================================== */

.review {
  display: flex;
  flex-direction: column;
  gap: 12px;

  list-style: none;
}

.row {
  display: flex;
  align-items: flex-start;
  gap: 20px;

  padding: 20px 22px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.2);
  border-radius: 14px;
}

.row.missing {
  border-color: rgba(255, 78, 205, 0.55);
  background: rgba(255, 78, 205, 0.05);
}

.number {
  flex-shrink: 0;
  padding-top: 2px;

  color: var(--pink);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 2px;
}

.row-body {
  flex: 1;
  min-width: 0;

  display: flex;
  flex-direction: column;
  gap: 10px;
}

.row-body h2 {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}

.picked {
  align-self: flex-start;

  padding: 5px 12px;

  background: rgba(0, 229, 168, 0.14);
  border-radius: 99px;

  color: var(--mint);
  font-size: 12px;
  font-weight: 800;
}

.unanswered {
  align-self: flex-start;

  padding: 5px 12px;

  background: rgba(255, 78, 205, 0.14);
  border-radius: 99px;

  color: var(--pink);
  font-size: 12px;
  font-weight: 800;
}

.preview {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;

  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
}

.edit {
  flex-shrink: 0;

  padding: 8px 16px;

  background: transparent;
  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 8px;

  color: var(--text-secondary);
  font-family: inherit;
  font-size: 13px;
  font-weight: 700;

  cursor: pointer;
  transition: border-color 0.25s ease, color 0.25s ease, background 0.25s ease;
}

.edit:hover {
  border-color: var(--lavender);
  color: var(--text);
}

.edit.urgent {
  border-color: var(--pink);
  color: var(--pink);
}

.edit.urgent:hover {
  background: rgba(255, 78, 205, 0.12);
}

/* ========================================
   SUMMARY
======================================== */

.summary {
  position: sticky;
  top: 24px;

  display: flex;
  flex-direction: column;
  gap: 20px;

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

.meter-numbers {
  display: flex;
  align-items: baseline;
  gap: 10px;

  margin-bottom: 12px;
}

.meter-numbers strong {
  font-size: 40px;
  font-weight: 800;
  line-height: 1;
}

.meter-numbers span {
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 600;
}

.bar {
  height: 6px;

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

.notice {
  display: flex;
  flex-direction: column;
  gap: 6px;

  padding: 14px 16px;

  border: 1px solid;
  border-radius: 12px;

  font-size: 13px;
  line-height: 1.5;
}

.notice b {
  font-size: 13px;
  font-weight: 800;
}

.notice span {
  color: var(--text-secondary);
  font-weight: 500;
}

.notice.warning {
  background: rgba(255, 78, 205, 0.07);
  border-color: rgba(255, 78, 205, 0.4);
}

.notice.warning b {
  color: var(--pink);
}

.notice.missing-notice {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(197, 163, 255, 0.3);
}

.error {
  color: #FF9B9B;
  font-size: 13px;
  font-weight: 600;
}

.primary,
.ghost {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;

  padding: 16px 24px;

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

.spinner.small {
  width: 16px;
  height: 16px;

  border-color: rgba(23, 17, 38, 0.25);
  border-top-color: var(--bg);
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

@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }

  /* resumo com o botão sobe para antes da lista */
  .summary {
    position: static;
    order: -1;
  }
}

@media (max-width: 900px) {
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
    padding: 32px 5% 48px;
  }

  .row {
    flex-wrap: wrap;
    gap: 12px 16px;
    padding: 16px;
  }

  .edit {
    margin-left: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .spinner {
    animation-duration: 0.01ms !important;
  }

  .primary,
  .bar-fill {
    transition: none;
  }
}
</style>
