import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import ExperimentChoice from '@/views/ExperimentChoice.vue'
import QuizQuestionsView from '@/views/QuizQuestionsView.vue'
import QuestionnairesView from '@/views/QuestionnairesView.vue'
import QuestionnaireDetailView from '@/views/QuestionnaireDetailView.vue'
import JudgmentView from '@/views/JudgmentView.vue'
import FinalizeView from '@/views/FinalizeView.vue'
import NewExperimentView from '@/views/NewExperimentView.vue'
import ResultView from '@/views/ResultView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AboutView
    },

    {
      path: '/quiz',
      name: 'quiz',
      component: ExperimentChoice
    },
    {
      path: '/quiz/novo/perguntas',
      name: 'quiz novas perguntas',
      component: QuizQuestionsView
    },
    {
      path: '/questionarios',
      name: 'questionarios',
      component: QuestionnairesView
    },
     {
      path: '/questionarios/:id',
      name: 'questionarios detail',
      component: QuestionnaireDetailView
    },
    {
      path: '/quiz/julgamento',
      name: 'julgamento',
      component: JudgmentView
    },
    {
      path: '/quiz/finalizar',
      name: 'finalizar',
      component: FinalizeView
    },
    {
      path: '/quiz/novo',
      name: 'quiz novo',
      component: NewExperimentView
    },
    {
      path: '/quiz/resultado',
      name: 'resultado quiz',
      component: ResultView
    }
  ],
})

export default router
