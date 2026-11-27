
<script setup lang="ts">
import GradientBackground from '@/components/animate-ui/backgrounds/gradient/GradientBackground.vue'

const startQuiz = () => {
  window.location.href = '/quiz'
}

const scrollToSection = (id: string) => {
  document.getElementById(id)?.scrollIntoView({
    behavior: 'smooth'
  })
}
</script>

<template>
  <main class="about-page">

    <!-- BACKGROUND -->
    <GradientBackground
      class="gradient-background"
      :transition="{
        duration: 25,
        ease: 'easeInOut',
        repeat: Infinity
      }"
    />

    <!-- HEADER -->
    <header class="header">
      <a href="/" class="brand">
        <img
          src="../assets/eliza-logo.png"
          alt="Logo ELIZA"
          class="brand-logo"
        />
        <span>ELIZA</span>
      </a>

      <nav class="navigation">
        <a href="/">Home</a>
        <a href="/sobre" class="active">Sobre</a>
      </nav>

      <button class="header-button" @click="startQuiz">
        Começar experimento
        <span>→</span>
      </button>
    </header>

    <!-- HERO -->
    <section class="hero">
      <div class="hero-content">

        <div class="hero-text">
          <span class="eyebrow">
            SOBRE O PROJETO
          </span>

          <h1>
            Afinal, o que nos faz
            <span>parecer humanos?</span>
          </h1>

          <p>
            O ELIZA é um experimento interativo que investiga
            como percebemos a comunicação humana e as respostas
            produzidas por inteligência artificial.
          </p>

          <p>
            Aqui, você assume o papel de juiz e coloca sua própria
            percepção à prova: será que consegue identificar
            quem está por trás de cada resposta?
          </p>

          <button
            class="primary-button"
            @click="scrollToSection('como-funciona')"
          >
            Descubra como funciona
            <span>↓</span>
          </button>
        </div>

        <div class="hero-visual">
          <div class="logo-glow">
            <img
              src="../assets/eliza-logo.png"
              alt="Símbolo do ELIZA"
              class="hero-logo"
            />
          </div>

          <span class="visual-caption">
            HUMAN · AI · PERCEPTION
          </span>
        </div>

      </div>

      <div class="hero-bottom">
        <span>UMA EXPERIÊNCIA SOBRE A PERCEPÇÃO HUMANA</span>
        <span>SCROLL PARA EXPLORAR ↓</span>
      </div>
    </section>

    <!-- INTRODUCTION -->
    <section class="introduction section-container">

      <div class="section-heading">
        <span class="eyebrow">01 — A PROPOSTA</span>

        <h2>
          Mais do que identificar respostas,
          <span>questionar percepções.</span>
        </h2>
      </div>

      <div class="introduction-content">
        <p>
          Com o avanço da inteligência artificial, textos e
          respostas produzidos por máquinas estão cada vez mais
          presentes no nosso cotidiano. Muitas vezes, essas
          respostas podem apresentar características semelhantes
          às da comunicação humana.
        </p>

        <p>
          Mas até que ponto conseguimos perceber a diferença?
          O ELIZA propõe uma experiência em que você precisa
          observar, interpretar e decidir qual resposta acredita
          ter sido escrita por uma pessoa e qual foi produzida
          por uma inteligência artificial.
        </p>
      </div>

    </section>

    <!-- OBJECTIVE -->
    <section class="objective section-container">

      <div class="objective-visual">
        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>

        <div class="orbit-center">
          <span>?</span>
        </div>

        <div class="orbit-label label-human">
          HUMAN
        </div>

        <div class="orbit-label label-ai">
          ARTIFICIAL
        </div>
      </div>

      <div class="objective-content">
        <span class="eyebrow">02 — NOSSO OBJETIVO</span>

        <h2>
          Onde termina a
          <span>percepção?</span>
        </h2>

        <p>
          O objetivo do ELIZA é explorar a capacidade humana
          de distinguir respostas humanas das produzidas por IA,
          observando como linguagem, contexto e interpretação
          influenciam nossas decisões.
        </p>

        <p>
          Não buscamos provar que uma máquina pensa ou sente
          como um ser humano. Queremos investigar como as pessoas
          percebem essa semelhança durante uma interação.
        </p>
      </div>

    </section>

    <!-- HOW IT WORKS -->
    <section id="como-funciona" class="how-section">

      <div class="section-container">

        <div class="section-heading centered">
          <span class="eyebrow">03 — COMO FUNCIONA</span>

          <h2>
            Três etapas.
            <span>Uma decisão.</span>
          </h2>

          <p>
            Sua missão é analisar as respostas e descobrir
            qual delas foi produzida por um humano.
          </p>
        </div>

        <div class="steps">

          <article class="step-card">
            <div class="step-number">01</div>

            <div class="step-icon">
              <span>✎</span>
            </div>

            <h3>Respostas</h3>

            <p>
              Perguntas são apresentadas e respondidas por
              uma pessoa e por uma inteligência artificial.
            </p>

            <span class="step-caption">
              COLETA DE RESPOSTAS
            </span>
          </article>

          <div class="step-connector">→</div>

          <article class="step-card">
            <div class="step-number">02</div>

            <div class="step-icon">
              <span>◉</span>
            </div>

            <h3>Julgamento</h3>

            <p>
              Você analisa duas respostas anônimas e escolhe
              qual acredita ser humana e qual acredita ser de IA.
            </p>

            <span class="step-caption">
              ANÁLISE E DECISÃO
            </span>
          </article>

          <div class="step-connector">→</div>

          <article class="step-card">
            <div class="step-number">03</div>

            <div class="step-icon">
              <span>⌁</span>
            </div>

            <h3>Resultado</h3>

            <p>
              Ao final, suas escolhas são comparadas com as
              respostas originais e você descobre seu desempenho.
            </p>

            <span class="step-caption">
              RESULTADO FINAL
            </span>
          </article>

        </div>
      </div>
    </section>

    <!-- MODES -->
    <section class="modes section-container">

      <div class="section-heading">
        <span class="eyebrow">04 — ESCOLHA SUA EXPERIÊNCIA</span>

        <h2>
          Duas maneiras de
          <span>participar.</span>
        </h2>

        <p>
          Você pode construir um experimento completo ou
          começar diretamente pelo julgamento.
        </p>
      </div>

      <div class="mode-grid">

        <article class="mode-card">
          <div class="mode-top">
            <span class="mode-tag">EXPERIÊNCIA COMPLETA</span>
            <span class="mode-index">01</span>
          </div>

          <div class="mode-icon">✧</div>

          <h3>Novo experimento</h3>

          <p>
            Comece do zero. As perguntas serão respondidas
            por um humano e por uma IA. Depois, você assume
            o papel de juiz e analisa todas as respostas.
          </p>

          <ul>
            <li>Responder às perguntas</li>
            <li>Gerar respostas da IA</li>
            <li>Realizar o julgamento</li>
            <li>Conferir o resultado</li>
          </ul>

          <button class="mode-button" @click="startQuiz">
            Começar do zero
            <span>→</span>
          </button>
        </article>

        <article class="mode-card featured">
          <div class="mode-top">
            <span class="mode-tag">MAIS RÁPIDO</span>
            <span class="mode-index">02</span>
          </div>

          <div class="mode-icon">◈</div>

          <h3>Questionários prontos</h3>

          <p>
            Escolha um questionário que já possui respostas
            humanas e de IA. Você não precisa passar pela
            etapa de perguntas: pode ir direto ao julgamento.
          </p>

          <ul>
            <li>Perguntas já cadastradas</li>
            <li>Respostas previamente coletadas</li>
            <li>Julgamento imediato</li>
            <li>Resultado ao finalizar</li>
          </ul>

          <button
            class="mode-button"
            @click="$router.push('/questionarios')"
          >
            Explorar questionários
            <span>→</span>
          </button>
        </article>

      </div>
    </section>

    <!-- INSPIRATION -->
    <section class="inspiration">

      <div class="inspiration-content">
        <span class="eyebrow">05 — NOSSA INSPIRAÇÃO</span>

        <h2>
          Uma homenagem à história da
          <span>interação entre humanos e máquinas.</span>
        </h2>

        <p>
          O nome ELIZA faz referência ao programa desenvolvido
          por Joseph Weizenbaum no MIT, na década de 1960.
          Considerado um dos primeiros programas de conversação,
          ele simulava diálogos por meio de padrões e regras
          de linguagem.
        </p>

        <p>
          A experiência original levantou uma questão que continua
          relevante: por que atribuímos características humanas
          a sistemas que se comunicam conosco?
        </p>

        <p>
          Inspirado por essa reflexão, nosso projeto propõe
          uma nova perspectiva sobre a relação entre linguagem,
          percepção e inteligência artificial.
        </p>

        <a
          href="https://findingeliza.org/about.html"
          target="_blank"
          rel="noopener noreferrer"
          class="inspiration-link"
        >
          Conheça a história do ELIZA original ↗
        </a>
      </div>

      <div class="inspiration-mark">
        <img
          src="../assets/eliza-logo.png"
          alt=""
        />
        <span>ELIZA</span>
        <small>1966 — PRESENTE</small>
      </div>

    </section>

    <!-- FINAL CTA -->
    <section class="final-cta">
      <span class="eyebrow">SUA PERCEPÇÃO SERÁ COLOCADA À PROVA</span>

      <h2>
        Você está pronto para
        <span>julgar?</span>
      </h2>

      <p>
        Descubra se consegue distinguir a comunicação humana
        da inteligência artificial.
      </p>

      <button class="primary-button" @click="startQuiz">
        Iniciar experiência
        <span>→</span>
      </button>
    </section>

    <!-- FOOTER -->
    <footer class="footer">
      <a href="/" class="footer-brand">ELIZA</a>

      <span>
        Um experimento sobre percepção humana e inteligência artificial.
      </span>

      <a href="/">Voltar ao início ↑</a>
    </footer>

  </main>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&display=swap');

:global(html) {
  scroll-behavior: smooth;
  scroll-padding-top: 74px;
}

:global(body) {
  margin: 0;
  background: #171126;
  color: #F5F1FA;
  font-family: 'Montserrat', sans-serif;
}

.about-page {
  --background: #171126;
  --purple: #3900A8;
  --purple-light: #8B2BFF;
  --lavender: #C5A3FF;
  --pink: #F12ACB;
  --cyan: #00E6B8;
  --text: #F5F1FA;
  --secondary: #C5BBD3;

  position: relative;
  isolation: isolate;
  min-height: 100vh;
  overflow-x: clip;
  background: transparent;
}

.gradient-background {
  position: fixed;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100vh;
  pointer-events: none;
}

/* HEADER */

.header {
  position: sticky;
  top: 0;
  z-index: 100;

  height: 74px;
  padding: 0 5%;

  display: flex;
  align-items: center;
  justify-content: space-between;

  background: rgba(23, 17, 38, 0.92);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;

  background: linear-gradient(
    90deg,
    transparent,
    rgba(139, 43, 255, 0.7),
    transparent
  );
}

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  color: var(--lavender);
  font-size: 21px;
  font-weight: 700;
  letter-spacing: 7px;
}

.brand-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.navigation {
  display: flex;
  gap: 35px;
}

.navigation a {
  color: var(--secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  transition: color 0.3s;
}

.navigation a:hover,
.navigation a.active {
  color: white;
}

.header-button {
  display: flex;
  align-items: center;
  gap: 12px;

  padding: 11px 18px;

  color: var(--cyan);
  background: transparent;
  border: 1px solid var(--cyan);
  border-radius: 8px;

  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.3s;
}

.header-button:hover {
  background: var(--cyan);
  color: var(--background);
}

/* COMMON */

.section-container {
  position: relative;
  z-index: 1;
  width: min(1180px, 90%);
  margin: 0 auto;
}

.eyebrow {
  display: block;
  color: var(--pink);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 4px;
  line-height: 1.7;
}

.section-heading h2 {
  margin: 20px 0;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.15;
  letter-spacing: -1.5px;
}

.section-heading h2 span,
.hero-text h1 span,
.objective-content h2 span,
.inspiration-content h2 span,
.final-cta h2 span {
  color: transparent;
  background: linear-gradient(
    100deg,
    var(--pink),
    var(--lavender)
  );
  background-clip: text;
  -webkit-background-clip: text;
}

.section-heading > p {
  color: var(--secondary);
  font-size: 16px;
  line-height: 1.7;
  max-width: 650px;
}

/* HERO */

.hero {
  position: relative;
  z-index: 1;

  min-height: calc(100vh - 74px);
  padding: 80px 7% 60px;

  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-content {
  width: 100%;
  max-width: 1350px;
  margin: auto;

  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  align-items: center;
  gap: 60px;
}

.hero-text {
  max-width: 720px;
}

.hero-text h1 {
  margin: 25px 0;

  font-size: clamp(40px, 5vw, 65px);
  line-height: 1.08;
  letter-spacing: -2px;
}

.hero-text p {
  max-width: 650px;
  color: var(--secondary);
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 16px;
}

.primary-button {
  display: inline-flex;
  align-items: center;
  gap: 20px;

  margin-top: 20px;
  padding: 16px 23px;

  color: #101522;
  background: var(--cyan);
  border-radius: 8px;

  font-size: 14px;
  font-weight: 800;
  cursor: pointer;
  transition: 0.3s;
}

.primary-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 230, 184, 0.2);
}

.primary-button span {
  font-size: 20px;
}

.hero-visual {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.logo-glow {
  position: relative;
  width: min(340px, 28vw);
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  isolation: isolate;
}

.logo-glow::before {
  content: '';
  position: absolute;
  inset: -30%;
  z-index: -1;

  background: radial-gradient(
    circle,
    rgba(91, 0, 255, 0.4),
    rgba(57, 0, 168, 0.15) 45%,
    transparent 70%
  );

  filter: blur(25px);
}

.hero-logo {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 25px rgba(139, 43, 255, 0.35));
}

.visual-caption {
  margin-top: 25px;
  color: var(--lavender);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 7px;
}

.hero-bottom {
  position: absolute;
  bottom: 25px;
  left: 7%;
  right: 7%;

  display: flex;
  justify-content: space-between;

  color: rgba(197, 187, 211, 0.5);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 2px;
}

/* INTRODUCTION */

.introduction {
  padding-top: 130px;
  padding-bottom: 130px;

  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 90px;
}

.introduction .section-heading h2 {
  max-width: 500px;
}

.introduction-content {
  padding-top: 35px;
}

.introduction-content p {
  margin-bottom: 25px;
  color: var(--secondary);
  font-size: 16px;
  line-height: 1.9;
}

/* OBJECTIVE */

.objective {
  padding-top: 90px;
  padding-bottom: 140px;

  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  align-items: center;
  gap: 100px;
}

.objective-content h2 {
  margin: 22px 0;
  font-size: clamp(36px, 4vw, 50px);
  line-height: 1.15;
}

.objective-content p {
  margin-bottom: 20px;
  color: var(--secondary);
  font-size: 15px;
  line-height: 1.9;
}

/* ORBIT */

.objective-visual {
  position: relative;
  width: 350px;
  height: 350px;
  margin: auto;

  display: flex;
  align-items: center;
  justify-content: center;
}

.orbit {
  position: absolute;
  border: 1px solid rgba(139, 43, 255, 0.55);
  border-radius: 50%;
}

.orbit-one {
  width: 210px;
  height: 210px;
  box-shadow: 0 0 30px rgba(139, 43, 255, 0.12);
}

.orbit-two {
  width: 320px;
  height: 320px;
  border-style: dashed;
  opacity: 0.55;
}

.orbit-center {
  width: 110px;
  height: 110px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: white;
  font-size: 65px;
  font-weight: 500;

  border-radius: 50%;
  background: radial-gradient(circle, #6425D9, #260064);
  box-shadow: 0 0 50px rgba(139, 43, 255, 0.4);
}

.orbit-label {
  position: absolute;
  padding: 9px 14px;

  background: #211637;
  border: 1px solid rgba(197, 163, 255, 0.3);
  border-radius: 20px;

  font-size: 10px;
  font-weight: 800;
  letter-spacing: 2px;
}

.label-human {
  top: 35px;
  left: 15px;
  color: var(--cyan);
}

.label-ai {
  right: 0;
  bottom: 45px;
  color: var(--pink);
}

/* HOW IT WORKS */

.how-section {
  position: relative;
  z-index: 1;

  padding: 120px 0 140px;

  background: rgba(24, 14, 48, 0.55);
  border-top: 1px solid rgba(139, 43, 255, 0.15);
  border-bottom: 1px solid rgba(139, 43, 255, 0.15);
}

.centered {
  text-align: center;
}

.centered > p {
  margin: 0 auto;
}

.steps {
  margin-top: 75px;

  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: center;
  gap: 20px;
}

.step-card {
  position: relative;
  min-height: 330px;
  padding: 35px 28px;

  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(197, 163, 255, 0.16);
  border-radius: 14px;

  transition: 0.3s;
}

.step-card:hover {
  transform: translateY(-7px);
  border-color: rgba(197, 163, 255, 0.55);
  background: rgba(139, 43, 255, 0.07);
}

.step-number {
  color: rgba(197, 163, 255, 0.55);
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 2px;
}

.step-icon {
  width: 58px;
  height: 58px;
  margin: 30px 0 25px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: var(--lavender);
  background: rgba(139, 43, 255, 0.15);
  border: 1px solid rgba(139, 43, 255, 0.4);
  border-radius: 12px;

  font-size: 28px;
}

.step-card h3 {
  margin-bottom: 15px;
  font-size: 21px;
}

.step-card p {
  color: var(--secondary);
  font-size: 13px;
  line-height: 1.8;
}

.step-caption {
  display: block;
  margin-top: 25px;

  color: var(--pink);
  font-size: 9px;
  font-weight: 800;
  letter-spacing: 2px;
}

.step-connector {
  color: var(--purple-light);
  font-size: 25px;
}

/* MODES */

.modes {
  padding-top: 130px;
  padding-bottom: 140px;
}

.mode-grid {
  margin-top: 55px;

  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
}

.mode-card {
  padding: 35px;

  background: rgba(255, 255, 255, 0.025);
  border: 1px solid rgba(197, 163, 255, 0.18);
  border-radius: 15px;

  transition: 0.3s;
}

.mode-card:hover {
  transform: translateY(-5px);
  border-color: rgba(197, 163, 255, 0.5);
}

.mode-card.featured {
  background: linear-gradient(
    145deg,
    rgba(139, 43, 255, 0.15),
    rgba(241, 42, 203, 0.035)
  );

  border-color: rgba(139, 43, 255, 0.55);
}

.mode-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mode-tag {
  color: var(--pink);
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 2px;
}

.mode-index {
  color: rgba(197, 163, 255, 0.5);
  font-size: 14px;
  font-weight: 800;
}

.mode-icon {
  margin: 35px 0 20px;
  color: var(--lavender);
  font-size: 35px;
}

.mode-card h3 {
  margin-bottom: 15px;
  font-size: 25px;
}

.mode-card > p {
  min-height: 90px;
  color: var(--secondary);
  font-size: 14px;
  line-height: 1.8;
}

.mode-card ul {
  margin: 25px 0 30px;
  padding: 0;
  list-style: none;
}

.mode-card li {
  margin-bottom: 13px;
  color: var(--secondary);
  font-size: 13px;
}

.mode-card li::before {
  content: '✓';
  margin-right: 12px;
  color: var(--cyan);
  font-weight: 800;
}

.mode-button {
  width: 100%;
  padding: 15px 18px;

  display: flex;
  justify-content: space-between;
  align-items: center;

  color: white;
  background: rgba(139, 43, 255, 0.17);
  border: 1px solid rgba(139, 43, 255, 0.45);
  border-radius: 8px;

  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.3s;
}

.mode-button:hover {
  background: var(--purple);
  border-color: var(--purple-light);
}

/* INSPIRATION */

.inspiration {
  position: relative;
  z-index: 1;

  padding: 110px 8%;

  display: grid;
  grid-template-columns: 1.4fr 0.6fr;
  align-items: center;
  gap: 70px;

  background: rgba(24, 14, 48, 0.55);
  border-top: 1px solid rgba(139, 43, 255, 0.15);
}

.inspiration-content {
  max-width: 750px;
}

.inspiration-content h2 {
  margin: 22px 0;
  font-size: clamp(32px, 4vw, 45px);
  line-height: 1.2;
}

.inspiration-content p {
  margin-bottom: 20px;
  color: var(--secondary);
  font-size: 14px;
  line-height: 1.9;
}

.inspiration-link {
  display: inline-block;
  margin-top: 12px;

  color: var(--cyan);
  text-decoration: none;
  font-size: 13px;
  font-weight: 700;
}

.inspiration-link:hover {
  text-decoration: underline;
}

.inspiration-mark {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.inspiration-mark img {
  width: 180px;
  height: 180px;
  object-fit: contain;
  filter: drop-shadow(0 0 25px rgba(139, 43, 255, 0.35));
}

.inspiration-mark span {
  margin-top: 15px;
  font-size: 30px;
  font-weight: 700;
  letter-spacing: 9px;
}

.inspiration-mark small {
  margin-top: 10px;
  color: var(--lavender);
  font-size: 10px;
  letter-spacing: 4px;
}

/* FINAL CTA */

.final-cta {
  position: relative;
  z-index: 1;

  padding: 120px 7%;
  text-align: center;
}

.final-cta h2 {
  margin: 20px auto;
  max-width: 750px;
  font-size: clamp(36px, 5vw, 55px);
  line-height: 1.15;
}

.final-cta p {
  max-width: 550px;
  margin: 0 auto;

  color: var(--secondary);
  font-size: 15px;
  line-height: 1.8;
}

/* FOOTER */

.footer {
  position: relative;
  z-index: 1;

  min-height: 85px;
  padding: 20px 5%;

  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;

  border-top: 1px solid rgba(139, 43, 255, 0.2);
  background: rgba(23, 17, 38, 0.75);
}

.footer-brand {
  color: var(--lavender);
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 5px;
  text-decoration: none;
}

.footer span,
.footer > a:last-child {
  color: var(--secondary);
  font-size: 11px;
  text-decoration: none;
}

/* TABLET */

@media (max-width: 900px) {
  .hero-content {
    grid-template-columns: 1fr 0.7fr;
    gap: 25px;
  }

  .logo-glow {
    width: 260px;
  }

  .introduction,
  .objective {
    gap: 45px;
  }

  .steps {
    grid-template-columns: 1fr;
  }

  .step-connector {
    display: none;
  }

  .step-card {
    min-height: auto;
  }

  .inspiration {
    gap: 30px;
  }
}

/* MOBILE */

@media (max-width: 650px) {
  .header {
    height: 68px;
    padding: 0 5%;
  }

  .brand {
    font-size: 17px;
    letter-spacing: 4px;
  }

  .brand-logo {
    width: 42px;
    height: 42px;
  }

  .navigation {
    display: none;
  }

  .header-button {
    padding: 10px 12px;
    font-size: 10px;
  }

  .hero {
    min-height: auto;
    padding: 80px 6% 100px;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 50px;
  }

  .hero-text {
    text-align: center;
  }

  .hero-text h1 {
    font-size: 39px;
  }

  .hero-text p {
    font-size: 14px;
  }

  .logo-glow {
    width: 230px;
  }

  .visual-caption {
    font-size: 9px;
    letter-spacing: 4px;
  }

  .hero-bottom {
    font-size: 7px;
    letter-spacing: 1px;
  }

  .introduction,
  .objective {
    padding-top: 85px;
    padding-bottom: 85px;
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .introduction-content {
    padding-top: 0;
  }

  .introduction-content p,
  .objective-content p {
    font-size: 14px;
  }

  .objective-visual {
    width: 280px;
    height: 280px;
  }

  .orbit-one {
    width: 180px;
    height: 180px;
  }

  .orbit-two {
    width: 260px;
    height: 260px;
  }

  .orbit-center {
    width: 90px;
    height: 90px;
  }

  .label-human {
    left: 0;
  }

  .label-ai {
    right: 0;
  }

  .how-section,
  .modes {
    padding-top: 85px;
    padding-bottom: 90px;
  }

  .steps {
    margin-top: 40px;
  }

  .mode-grid {
    grid-template-columns: 1fr;
  }

  .mode-card {
    padding: 25px;
  }

  .mode-card > p {
    min-height: auto;
  }

  .inspiration {
    padding: 85px 6%;
    grid-template-columns: 1fr;
  }

  .inspiration-mark img {
    width: 140px;
    height: 140px;
  }

  .final-cta {
    padding: 90px 6%;
  }

  .footer {
    flex-direction: column;
    text-align: center;
    padding: 30px 6%;
  }
}

@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
</style>
