import Vue from 'vue'
import Router from 'vue-router'

import Search from '@/views/Search.vue'
import PostExo from '@/views/PostExo.vue'
import PostCorrection from '@/views/PostCorrection.vue'
import ExerciceDetail from '@/views/ExerciceDetail.vue'
import CorrectionDetail from '@/views/CorrectionDetail.vue'
import ExerciceCorrections from '@/views/ExerciceCorrections.vue'

import Profile from '@/views/Profile.vue'
import MoneyBox from '@/views/MoneyBox.vue'
import Recharge from '@/views/Recharge.vue'
import MyExercices from '@/views/MyExercices.vue'
import MyCorrections from '@/views/MyCorrections.vue'

import MentionsLegales from '@/views/MentionsLegales.vue'
import CGV from '@/views/CGV.vue'
import CGU from '@/views/CGU.vue'
import PDC from '@/views/PDC.vue'
import Presentation from '@/views/Presentation.vue'
import StandardsQualite from '@/views/StandardsQualite.vue'

import Register from '@/views/Register.vue'
import Login from '@/views/Login.vue'

import store from '@/store'
import api from '@/services/api'

Vue.use(Router)

const ifNotAuthenticated = (to, from, next) => {
  if (!store.getters['authentication/isAuthenticated']) {
    next()
    return
  } else {
    next(from.name)
  }
}

const ifAuthenticated = (to, from, next) => {
  store.dispatch('general/updateConstants')
  if (store.getters['authentication/isAuthenticated']) {
    let token = store.state.authentication.token
    api.defaults.headers['Authorization'] = 'Bearer ' + token
    next()
    return
  } else {
    next('/se-connecter')
  }
}

export default new Router({
  mode: 'history',
  base: '/',
  routes: [
    {
      path: '/',
      name: 'home',
      props: true,
      component: Search
    },
    {
      path: '/exercice/:id/',
      name: 'exercice',
      component: ExerciceDetail,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/exercice/:id/corrections/',
      name: 'exo-corrections',
      component: ExerciceCorrections,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/correction/:id/',
      name: 'correction',
      component: CorrectionDetail,
      props: true,
      beforeEnter: ifAuthenticated
    },
    // {
    //   path: '/rechercher-un-exo/',
    //   name: 'search',
    //   props: true,
    //   component: Search
    // },
    {
      path: '/demander-une-correction/',
      name: 'post-exo',
      component: PostExo,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/poster-une-correction/',
      name: 'post-correc',
      component: PostCorrection,
      props: true,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/mon-compte/',
      name: 'profile',
      component: Profile,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/mon-compte/ma-tirelire/',
      name: 'tirelire',
      component: MoneyBox,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/mon-compte/ma-tirelire/recharger/',
      name: 'recharge',
      component: Recharge,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/mon-compte/mes-exercices/',
      name: 'mes-exercices',
      component: MyExercices,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/mon-compte/mes-corrections/',
      name: 'mes-corrections',
      component: MyCorrections,
      beforeEnter: ifAuthenticated
    },
    {
      path: '/creer-un-compte/',
      name: 'register',
      component: Register,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/se-connecter/',
      name: 'login',
      component: Login,
      beforeEnter: ifNotAuthenticated
    },
    {
      path: '/mentions-legales',
      name: 'mentions-legales',
      component: MentionsLegales
    },
    {
      path: '/cgu',
      name: 'cgu',
      component: CGU
    },
    {
      path: '/cgv',
      name: 'cgv',
      component: CGV
    },
    {
      path: '/politique-de-confidentialite',
      name: 'pdc',
      component: PDC
    },
    {
      path: '/presentation-du-site',
      name: 'presentation',
      component: Presentation
    },
    {
      path: '/standards-qualite',
      name: 'standards-qualite',
      component: StandardsQualite
    },
    {
      path: '/*',
      name: 'others',
      component: Search
    }
  ],
  scrollBehavior() {
    return new Promise(resolve => {
      setTimeout(() => {
        resolve({ x: 0, y: 0 })
      }, 180)
    })
  }
})
