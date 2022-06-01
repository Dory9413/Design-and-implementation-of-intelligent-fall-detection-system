import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Main Menu',
        component: () => import('../components/Main')
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../components/Login')
    },
    {
        path: '/signup',
        name: 'Signup',
        component: () => import('../components/Signup')
    },
    {
        path: '/signup/contacts',
        name: 'Contacts',
        component: () => import('../components/Contacts')
    },
    {
        path: '/panel',
        name: 'Panel',
        component: () => import('../components/Panel')
    },
]

const router = new VueRouter({
    routes
})

export default router