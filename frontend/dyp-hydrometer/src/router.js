import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home.vue'
import Hydrometer from './components/Hydrometer.vue';
import Profile from './components/Profile.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/hydrometers/:id',
      name: 'Hydrometer',
      component: Hydrometer,
    },
    {
        path: '/profiles/:id',
        name: 'Profile',
        component: Profile,
      },
  ],
});