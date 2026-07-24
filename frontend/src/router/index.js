import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AdminLayout from '@/components/layout/AdminLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/auth/LoginView.vue'),
      meta: { requiresAuth: false },
    },
    {
      path: '/',
      component: AdminLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/vehiculos',
        },
        // Vehículos
        {
          path: 'vehiculos',
          name: 'Gestión de Vehículos',
          component: () => import('@/views/vehiculos/GestionarVehiculos.vue'),
        },
        {
          path: 'vehiculos/crear',
          name: 'Crear Vehículo',
          component: () => import('@/views/vehiculos/CrearVehiculo.vue'),
        },
        // Gastos
        {
          path: 'gastos',
          name: 'Gestión de Gastos',
          component: () => import('@/views/gastos/GestionarGastos.vue'),
        },
        {
          path: 'gastos/crear',
          name: 'Crear Gasto',
          component: () => import('@/views/gastos/CrearGasto.vue'),
        },
        {
          path: 'gastos/:id/editar',
          name: 'Editar Gasto',
          component: () => import('@/views/gastos/EditarGasto.vue'),
        },
        {
          path: 'gastos/:id/detalle',
          name: 'Detalle del Gasto',
          component: () => import('@/views/gastos/DetalleGasto.vue'),
        },
        // Tipos de Gasto
        {
          path: 'tipos-gasto',
          name: 'Tipos de Gasto',
          component: () => import('@/views/tipos/GestionarTipos.vue'),
        },
        {
          path: 'tipos-gasto/crear',
          name: 'Crear Tipo de Gasto',
          component: () => import('@/views/tipos/CrearTipo.vue'),
        },
        // Proveedores
        {
          path: 'proveedores',
          name: 'Gestión de Proveedores',
          component: () => import('@/views/proveedores/GestionarProveedores.vue'),
        },
        {
          path: 'proveedores/crear',
          name: 'Crear Proveedor',
          component: () => import('@/views/proveedores/CrearProveedor.vue'),
        },
      ],
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login' })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
