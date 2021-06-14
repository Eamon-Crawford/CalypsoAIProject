import { createWebHistory, createRouter } from 'vue-router';
import CsvHome from '@/components/CsvHome.vue';
import ViewCsv from '@/components/ViewCsv.vue';
import StatsCsv from '@/components/StatsCsv.vue';
import PageNotFound from '@/components/PageNotFound.vue';
// import About from "@/views/About.vue";

const routes = [
  {
    path: '/',
    name: 'CsvHome',
    component: CsvHome,
  },
  {
    path: '/csv/view/:name',
    name: 'ViewCsv',
    component: ViewCsv,
  },
  {
    path: '/csv/stats/:name',
    name: 'StatsCsv',
    component: StatsCsv,
  },
  {
    path: '/:catchAll(.*)*',
    name: 'PageNotFound',
    component: PageNotFound,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
