<script setup lang="ts">
defineProps<{
  active?: 'novo' | 'questionarios'
}>()
</script>

<template>
  <aside class="sidebar">

    <RouterLink to="/" class="sb-brand">
      <img
        src="../assets/eliza-logo.png"
        alt="ELIZA logo"
        class="sb-logo"
      />
      <span class="sb-name">ELIZA</span>
    </RouterLink>

    <span class="sb-label">EXPERIMENT</span>

    <nav class="sb-nav">

      <RouterLink
        to="/quiz"
        class="sb-item"
        :class="{ active: active === 'novo' }"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="12" r="9" />
          <path d="M12 3v18M3 12h18" />
        </svg>
        New experiment
      </RouterLink>

      <RouterLink
        to="/questionarios"
        class="sb-item"
        :class="{ active: active === 'questionarios' }"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="4" width="16" height="16" rx="3" />
          <path d="M8 9h8M8 13h8M8 17h5" />
        </svg>
        Questionnaires
      </RouterLink>

    </nav>

    <RouterLink to="/" class="sb-item sb-back">
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M3 12l9-9 9 9M5 10v10h14V10" />
      </svg>
      Back to home
    </RouterLink>

  </aside>
</template>

<style scoped>
.sidebar {
  position: sticky;
  top: 0;

  width: 280px;
  height: 100vh;
  flex-shrink: 0;

  display: flex;
  flex-direction: column;

  padding: 28px 20px;

  background: #120c20;
  border-right: 1px solid rgba(139, 43, 255, 0.35);
}

/* Brand */

.sb-brand {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 0 8px 34px;
  text-decoration: none;
}

.sb-logo {
  width: 46px;
  height: 46px;
  object-fit: contain;
}

.sb-name {
  color: #C5A3FF;
  font-size: 20px;
  font-weight: 700;
  letter-spacing: 6px;
}

/* Label */

.sb-label {
  padding: 0 12px;
  margin-bottom: 10px;

  color: #7D7096;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 3px;
}

/* Items */

.sb-nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.sb-item {
  display: flex;
  align-items: center;
  gap: 14px;

  padding: 13px 14px;
  border-radius: 10px;

  color: #C5BBD3;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;

  transition: background 0.25s ease, color 0.25s ease;
}

.sb-item svg {
  width: 20px;
  height: 20px;

  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.sb-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #F8F5FF;
}

.sb-item.active {
  background: rgba(57, 0, 168, 0.55);
  color: #FFFFFF;
  box-shadow: inset 3px 0 0 #00E5A8;
}

.sb-item.active svg {
  stroke: #00E5A8;
}

/* Back link fica no rodapé */

.sb-back {
  margin-top: auto;
  border: 1px solid rgba(197, 163, 255, 0.15);
}

/* Mobile: sidebar vira barra no topo */

@media (max-width: 900px) {
  .sidebar {
    position: static;
    width: 100%;
    height: auto;

    flex-direction: row;
    align-items: center;
    gap: 12px;

    padding: 12px 5%;
    border-right: none;
    border-bottom: 1px solid rgba(139, 43, 255, 0.35);

    overflow-x: auto;
  }

  .sb-brand {
    padding: 0;
  }

  .sb-name,
  .sb-label {
    display: none;
  }

  .sb-nav {
    flex-direction: row;
  }

  .sb-item {
    white-space: nowrap;
    padding: 10px 12px;
    font-size: 13px;
  }

  .sb-back {
    margin-top: 0;
    margin-left: auto;
  }
}
</style>
