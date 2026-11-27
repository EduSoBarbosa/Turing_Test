<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppSidebar from '@/components/AppSidebar.vue'

/* ========================================
   TIPOS
======================================== */

interface Questionnaire {
  id: number | string
  title: string
  description: string
  theme: string
  questionCount: number
  createdAt: string // ISO date
}

/* ========================================
   API (SUBSTITUA PELA SUA CHAMADA)
======================================== */

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms))

async function fetchQuestionnaires(): Promise<Questionnaire[]> {
  // TODO: troque pela sua API
  // const res = await fetch('/api/questionnaires')
  // return await res.json()

  await sleep(700)

  return [
    {
      id: 1,
      title: 'Memórias e emoções',
      description: 'Perguntas sobre lembranças, sentimentos e experiências pessoais.',
      theme: 'Emoções',
      questionCount: 10,
      createdAt: '2026-11-10'
    },
    {
      id: 2,
      title: 'Opiniões do dia a dia',
      description: 'Posicionamentos e escolhas em situações cotidianas.',
      theme: 'Cotidiano',
      questionCount: 10,
      createdAt: '2026-11-14'
    },
    {
      id: 3,
      title: 'Dilemas e decisões',
      description: 'Como as pessoas lidam com conflitos, dúvidas e mudanças de opinião.',
      theme: 'Dilemas',
      questionCount: 10,
      createdAt: '2026-11-18'
    },
    {
      id: 4,
      title: 'Futuro e tecnologia',
      description: 'Expectativas, medos e curiosidades sobre o que vem pela frente.',
      theme: 'Tecnologia',
      questionCount: 10,
      createdAt: '2026-11-22'
    }
  ]
}

/* ========================================
   ESTADO
======================================== */

const router = useRouter()

const status = ref<'loading' | 'ready' | 'error'>('loading')
const questionnaires = ref<Questionnaire[]>([])
const search = ref('')

async function load() {
  status.value = 'loading'

  try {
    questionnaires.value = await fetchQuestionnaires()
    status.value = 'ready'
  } catch {
    status.value = 'error'
  }
}

onMounted(load)

const filtered = computed(() => {
  const term = search.value.trim().toLowerCase()

  if (!term) return questionnaires.value

  return questionnaires.value.filter((q) =>
    [q.title, q.description, q.theme].some((field) =>
      field.toLowerCase().includes(term)
    )
  )
})

const formatDate = (iso: string) =>
  new Date(iso + 'T00:00:00').toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })

const openDetails = (id: number | string) => {
  router.push(`/questionarios/${id}`)
}
</script>

<template>
  <div class="app-shell">

    <AppSidebar active="questionarios" />

    <main class="content">

      <!-- TOP BAR -->
      <header class="topbar">
        <div class="breadcrumb">
          Biblioteca / <strong>Questionários</strong>
        </div>
      </header>

      <!-- BODY -->
      <section class="body">

        <span class="eyebrow">BIBLIOTECA</span>

        <h1>Questionários prontos</h1>

        <p class="lead">
          Escolha um conjunto já respondido por um humano e por uma IA
          e vá direto para a etapa de julgamento.
        </p>

        <!-- SEARCH -->
        <div v-if="status === 'ready'" class="toolbar">

          <label class="search">
            <svg viewBox="0 0 24 24" aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <path d="M20 20l-3.5-3.5" />
            </svg>
            <input
              v-model="search"
              type="search"
              placeholder="Buscar por título, tema ou descrição…"
              aria-label="Buscar questionários"
            />
          </label>

          <span class="count">
            {{ filtered.length }}
            {{ filtered.length === 1 ? 'questionário' : 'questionários' }}
          </span>

        </div>

        <!-- LOADING -->
        <div v-if="status === 'loading'" class="grid" aria-busy="true">
          <div v-for="n in 4" :key="n" class="card skeleton-card">
            <div class="skeleton" style="width: 40%; height: 12px" />
            <div class="skeleton" style="width: 75%; height: 22px" />
            <div class="skeleton" style="width: 95%" />
            <div class="skeleton" style="width: 70%" />
          </div>
        </div>

        <!-- ERROR -->
        <div v-else-if="status === 'error'" class="state">
          <p>Não foi possível carregar os questionários.</p>
          <button class="retry" @click="load">Tentar novamente</button>
        </div>

        <!-- EMPTY (nenhum cadastrado) -->
        <div
          v-else-if="questionnaires.length === 0"
          class="state"
        >
          <p>Ainda não há questionários prontos.</p>
          <a class="link" href="/quiz/novo" @click.prevent="router.push('/quiz/novo')">
            Criar um novo experimento
          </a>
        </div>

        <!-- EMPTY (busca sem resultado) -->
        <div v-else-if="filtered.length === 0" class="state">
          <p>Nenhum questionário encontrado para “{{ search }}”.</p>
          <button class="retry" @click="search = ''">Limpar busca</button>
        </div>

        <!-- LIST -->
        <div v-else class="grid">

          <article
            v-for="q in filtered"
            :key="q.id"
            class="card"
            tabindex="0"
            role="link"
            :aria-label="`Ver detalhes de ${q.title}`"
            @click="openDetails(q.id)"
            @keydown.enter="openDetails(q.id)"
          >

            <div class="card-top">
              <span class="theme">{{ q.theme }}</span>

              <svg class="doc-icon" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="4" y="3" width="16" height="18" rx="3" />
                <path d="M8 8h8M8 12h8M8 16h4" />
              </svg>
            </div>

            <h2>{{ q.title }}</h2>

            <p>{{ q.description }}</p>

            <ul class="meta">
              <li>{{ q.questionCount }} perguntas</li>
              <li>Humano + IA</li>
              <li>{{ formatDate(q.createdAt) }}</li>
            </ul>

            <span class="card-action">
              Ver detalhes <span aria-hidden="true">→</span>
            </span>

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

.breadcrumb strong {
  color: var(--text);
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
  margin-bottom: 36px;

  color: var(--text-secondary);
  font-size: 18px;
  font-weight: 500;
  line-height: 1.5;
}

/* ========================================
   TOOLBAR
======================================== */

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;

  margin-bottom: 26px;
}

.search {
  flex: 1;
  max-width: 480px;

  display: flex;
  align-items: center;
  gap: 12px;

  padding: 0 18px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(197, 163, 255, 0.25);
  border-radius: 12px;

  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.search:focus-within {
  border-color: var(--mint);
  box-shadow: 0 0 0 4px rgba(0, 229, 168, 0.12);
}

.search svg {
  width: 20px;
  height: 20px;
  flex-shrink: 0;

  fill: none;
  stroke: #8E82A6;
  stroke-width: 1.8;
  stroke-linecap: round;
}

.search input {
  flex: 1;
  min-width: 0;

  padding: 15px 0;

  background: transparent;
  border: none;
  outline: none;

  color: var(--text);
  font-family: inherit;
  font-size: 15px;
  font-weight: 500;
}

.search input::placeholder {
  color: #7D7096;
}

.count {
  color: #8E82A6;
  font-size: 13px;
  font-weight: 700;
  white-space: nowrap;
}

/* ========================================
   GRID / CARDS
======================================== */

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
}

.card {
  display: flex;
  flex-direction: column;

  padding: 28px;

  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 78, 205, 0.35);
  border-radius: 20px;

  cursor: pointer;
  outline: none;

  transition:
    transform 0.3s ease,
    border-color 0.3s ease,
    box-shadow 0.3s ease;
}

.card:hover,
.card:focus-visible {
  transform: translateY(-4px);

  border-color: var(--pink);
  box-shadow: 0 12px 40px rgba(255, 78, 205, 0.15);
}

.card:focus-visible {
  box-shadow: 0 0 0 4px rgba(255, 78, 205, 0.25);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-bottom: 20px;
}

.theme {
  padding: 6px 12px;

  background: rgba(255, 78, 205, 0.14);
  border-radius: 99px;

  color: var(--pink);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.doc-icon {
  width: 26px;
  height: 26px;

  fill: none;
  stroke: #8E82A6;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.card h2 {
  margin-bottom: 10px;

  font-size: 22px;
  font-weight: 800;
  line-height: 1.3;
}

.card p {
  margin-bottom: 20px;

  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.55;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;

  margin-bottom: auto;
  list-style: none;
}

.meta li {
  padding: 6px 12px;

  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 99px;

  color: #E2D6F5;
  font-size: 12px;
  font-weight: 700;
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;

  margin-top: 24px;
  padding-top: 18px;

  border-top: 1px solid rgba(197, 163, 255, 0.14);

  color: var(--pink);
  font-size: 15px;
  font-weight: 800;
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

.link {
  color: var(--mint);
  font-weight: 800;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}

/* Skeleton */

.skeleton-card {
  gap: 14px;
  min-height: 230px;
  cursor: default;
  border-color: rgba(197, 163, 255, 0.2);
}

.skeleton-card:hover {
  transform: none;
  box-shadow: none;
  border-color: rgba(197, 163, 255, 0.2);
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

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* ========================================
   RESPONSIVE
======================================== */

@media (max-width: 900px) {
  .app-shell {
    flex-direction: column;
  }

  .topbar {
    height: 64px;
    padding: 0 5%;
  }

  .body {
    padding: 32px 5%;
  }

  .toolbar {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .search {
    max-width: none;
  }

  .grid {
    grid-template-columns: 1fr;
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton {
    animation-duration: 0.01ms !important;
  }

  .card {
    transition: none;
  }
}
</style>
