<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'

/* ========================================
   TIPOS
======================================== */

interface Question {
  id: number
  text: string
}

interface QuestionnaireDetail {
  id: number | string
  title: string
  description: string
  theme: string
  createdAt: string // ISO date
  questions: Question[]
}

/* ========================================
   API
======================================== */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

// Devolva só as PERGUNTAS aqui. As respostas (humano/IA) não devem
// aparecer nesta tela, senão o julgamento perde o sentido.
async function fetchQuestionnaire(
  id: string
): Promise<QuestionnaireDetail | null> {
  // TODO: API (devolver null se não existir, ex.: status 404)
  // const res = await fetch(`/api/questionnaires/${id}`)
  // if (res.status === 404) return null
  // return await res.json()

  await sleep(600)

  if (!['1', '2', '3', '4'].includes(id)) return null

  return {
    id,
    title: 'Memórias e emoções',
    description:
      'Perguntas sobre lembranças, sentimentos e experiências pessoais. Cada pergunta tem uma resposta escrita por um humano e outra gerada por uma IA.',
    theme: 'Emoções',
    createdAt: '2026-11-10',
    questions: [
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
}

/* ========================================
   ESTADO
======================================== */

const route = useRoute()
const router = useRouter()

const status = ref<'loading' | 'ready' | 'notfound' | 'error'>('loading')
const questionnaire = ref<QuestionnaireDetail | null>(null)

async function load() {
  const id = String(route.params.id)

  status.value = 'loading'

  try {
    const data = await fetchQuestionnaire(id)

    if (!data) {
      status.value = 'notfound'
      return
    }

    questionnaire.value = data
    status.value = 'ready'
  } catch {
    status.value = 'error'
  }
}

// recarrega se o :id da rota mudar
watch(() => route.params.id, load, { immediate: true })

const formattedDate = computed(() =>
  questionnaire.value
    ? new Date(questionnaire.value.createdAt + 'T00:00:00').toLocaleDateString(
        'pt-BR',
        { day: '2-digit', month: 'long', year: 'numeric' }
      )
    : ''
)

const goBack = () => router.push('/questionarios')

// a JudgmentView lê o ?questionario= para saber que conjunto carregar
const startJudgment = () => {
  if (!questionnaire.value) return

  // começa um julgamento limpo (descarta ordem A/B e escolhas antigas)
  sessionStorage.removeItem('eliza:judgment')

  router.push({
    path: '/quiz/julgamento',
    query: { questionario: String(questionnaire.value.id) }
  })
}
</script>

<template>
  <div class="app-shell">

    <AppSidebar active="questionarios" />

    <main class="content">

      <!-- TOP BAR -->
      <header class="topbar">

        <div class="breadcrumb">
          <a href="/questionarios" @click.prevent="goBack">Questionários</a>
          /
          <strong>{{ questionnaire?.title ?? 'Detalhes' }}</strong>
        </div>

      </header>

      <section class="body">

        <button class="back" @click="goBack">
          <span aria-hidden="true">←</span> Voltar para a biblioteca
        </button>

        <!-- LOADING -->
        <div v-if="status === 'loading'" class="layout" aria-busy="true">
          <div class="main-col">
            <div class="skeleton" style="width: 30%; height: 12px" />
            <div class="skeleton" style="width: 60%; height: 40px" />
            <div class="skeleton" style="width: 90%" />
            <div class="skeleton" style="width: 75%" />
            <div
              v-for="n in 5"
              :key="n"
              class="skeleton"
              style="width: 100%; height: 64px; border-radius: 14px"
            />
          </div>
        </div>

        <!-- NOT FOUND / ERROR -->
        <div v-else-if="status === 'notfound'" class="state">
          <p>Questionário não encontrado.</p>
          <button class="outline" @click="goBack">
            Voltar para a biblioteca
          </button>
        </div>

        <div v-else-if="status === 'error'" class="state">
          <p>Não foi possível carregar este questionário.</p>
          <button class="outline" @click="load">Tentar novamente</button>
        </div>

        <!-- READY -->
        <div v-else-if="questionnaire" class="layout">

          <!-- QUESTIONS -->
          <div class="main-col">

            <span class="theme">{{ questionnaire.theme }}</span>

            <h1>{{ questionnaire.title }}</h1>

            <p class="lead">{{ questionnaire.description }}</p>

            <h2 class="section-title">
              Perguntas
              <span>{{ questionnaire.questions.length }}</span>
            </h2>

            <ol class="questions">
              <li
                v-for="(q, index) in questionnaire.questions"
                :key="q.id"
                class="question"
              >
                <span class="number">
                  {{ String(index + 1).padStart(2, '0') }}
                </span>
                <p>{{ q.text }}</p>
              </li>
            </ol>

          </div>

          <!-- SUMMARY -->
          <aside class="summary">

            <h3>Resumo</h3>

            <dl>
              <div>
                <dt>Perguntas</dt>
                <dd>{{ questionnaire.questions.length }}</dd>
              </div>
              <div>
                <dt>Respostas por pergunta</dt>
                <dd>2 (humano + IA)</dd>
              </div>
              <div>
                <dt>Criado em</dt>
                <dd>{{ formattedDate }}</dd>
              </div>
              <div>
                <dt>Tempo estimado</dt>
                <dd>~5 min</dd>
              </div>
            </dl>

            <div class="how">
              <span class="how-title">COMO FUNCIONA</span>
              <ol>
                <li>Você lê as duas respostas de cada pergunta.</li>
                <li>Aponta qual foi escrita pelo humano.</li>
                <li>No fim, vê seus acertos e erros.</li>
              </ol>
            </div>

            <button class="cta" @click="startJudgment">
              Iniciar julgamento
              <span aria-hidden="true">→</span>
            </button>

            <small>
              A origem das respostas só é revelada no resultado final.
            </small>

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

  background: rgba(23, 17, 38, 0.7);
  border-bottom: 1px solid rgba(139, 43, 255, 0.25);
}

.breadcrumb {
  color: #8E82A6;
  font-size: 14px;
  font-weight: 600;
}

.breadcrumb a {
  color: inherit;
  text-decoration: none;
}

.breadcrumb a:hover {
  color: var(--text);
}

.breadcrumb strong {
  color: var(--text);
}

/* ========================================
   BODY
======================================== */

.body {
  width: 100%;
  max-width: 1300px;

  padding: 40px 56px 64px;
}

.back {
  margin-bottom: 32px;
  padding: 0;

  background: none;
  border: none;

  color: var(--text-secondary);
  font-family: inherit;
  font-size: 14px;
  font-weight: 700;

  cursor: pointer;
  transition: color 0.25s ease;
}

.back:hover {
  color: var(--mint);
}

.layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 360px;
  gap: 40px;

  align-items: start;
}

.main-col {
  display: flex;
  flex-direction: column;
}

.theme {
  align-self: flex-start;

  margin-bottom: 18px;
  padding: 6px 12px;

  background: rgba(255, 78, 205, 0.14);
  border-radius: 99px;

  color: var(--pink);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
}

h1 {
  margin-bottom: 14px;

  font-size: clamp(30px, 3vw, 44px);
  font-weight: 800;
  letter-spacing: -1.2px;
  line-height: 1.15;
}

.lead {
  max-width: 720px;
  margin-bottom: 40px;

  color: var(--text-secondary);
  font-size: 17px;
  font-weight: 500;
  line-height: 1.6;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 12px;

  margin-bottom: 18px;

  font-size: 20px;
  font-weight: 800;
}

.section-title span {
  padding: 3px 11px;

  background: rgba(255, 255, 255, 0.08);
  border-radius: 99px;

  color: var(--text-secondary);
  font-size: 13px;
}

/* ========================================
   QUESTIONS
======================================== */

.questions {
  display: flex;
  flex-direction: column;
  gap: 12px;

  list-style: none;
}

.question {
  display: flex;
  align-items: center;
  gap: 20px;

  padding: 18px 22px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.2);
  border-radius: 14px;
}

.number {
  flex-shrink: 0;

  color: var(--pink);
  font-size: 15px;
  font-weight: 800;
  letter-spacing: 2px;
}

.question p {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.45;
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

.how-title {
  display: block;
  margin-bottom: 10px;

  color: #8E82A6;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 3px;
}

.how ol {
  display: flex;
  flex-direction: column;
  gap: 8px;

  padding-left: 18px;

  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  line-height: 1.45;
}

.cta {
  display: flex;
  align-items: center;
  justify-content: space-between;

  padding: 17px 26px;

  background: var(--mint);
  border: none;
  border-radius: 10px;

  color: var(--bg);
  font-family: inherit;
  font-size: 16px;
  font-weight: 800;

  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0, 229, 168, 0.3);

  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(0, 229, 168, 0.45);
}

.summary small {
  color: #8E82A6;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
}

/* ========================================
   STATES
======================================== */

.state {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;

  padding: 32px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.22);
  border-radius: 16px;

  color: var(--text-secondary);
  font-weight: 600;
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

.layout > .main-col > .skeleton {
  margin-bottom: 14px;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }

  /* resumo sobe para antes das perguntas */
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
    height: 64px;
    padding: 0 5%;
  }

  .breadcrumb {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .body {
    padding: 28px 5% 48px;
  }

  .question {
    padding: 16px;
    gap: 14px;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation-duration: 0.01ms !important;
  }

  .cta {
    transition: none;
  }
}
</style>