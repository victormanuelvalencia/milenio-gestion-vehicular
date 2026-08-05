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
        // Gastos
        {
          path: 'gastos',
          name: 'Gestión de Gastos',
          component: () => import('@/views/gastos/GestionarGastos.vue'),
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
        // Proveedores
        {
          path: 'proveedores',
          name: 'Gestión de Proveedores',
          component: () => import('@/views/proveedores/GestionarProveedores.vue'),
        },
        // Empresas
        {
          path: 'empresas',
          name: 'Gestión de Empresas',
          component: () => import('@/views/empresas/GestionarEmpresas.vue'),
        },
        // Conductores
        {
          path: 'conductores',
          name: 'Gestión de Conductores',
          component: () => import('@/views/conductores/GestionarConductores.vue'),
        },
        // Viajes
        {
          path: 'viajes',
          name: 'Gestión de Viajes',
          component: () => import('@/views/viajes/GestionarViajes.vue'),
        },
        {
          path: 'viajes/:id/detalle',
          name: 'Detalle del Viaje',
          component: () => import('@/views/viajes/DetalleViaje.vue'),
        },
        {
          path: 'viajes/:id/editar',
          name: 'Editar Viaje',
          component: () => import('@/views/viajes/EditarViaje.vue'),
        },
        {
          path: 'viajes/:id/gastos',
          name: 'Gastos del Viaje',
          component: () => import('@/views/viajes/GastosViaje.vue'),
        },
        // Mantenimientos
        {
          path: 'mantenimientos',
          name: 'Gestión de Mantenimientos',
          component: () => import('@/views/mantenimientos/GestionarMantenimientos.vue'),
        },
        // Programar Mantenimientos
        {
          path: 'mantenimientos-programados',
          name: 'Programar Mantenimientos',
          component: () => import('@/views/mantenimientos/ProgramarMantenimientos.vue'),
        },
        // Reportes
        {
          path: 'reportes',
          name: 'Reportes',
          component: () => import('@/views/reportes/ReportesView.vue'),
        },
        {
          path: 'reportes/gastos-por-vehiculo',
          name: 'Reporte Gastos por Vehículo',
          component: () => import('@/views/reportes/GastosPorVehiculo.vue'),
        },
        {
          path: 'reportes/gastos-por-mes',
          name: 'Reporte Gastos por Mes',
          component: () => import('@/views/reportes/GastosPorMes.vue'),
        },
        {
          path: 'reportes/utilidad-por-periodo',
          name: 'Reporte Utilidad por Período',
          component: () => import('@/views/reportes/UtilidadPorPeriodo.vue'),
        },
        {
          path: 'reportes/historial-vehiculo',
          name: 'Reporte Historial Vehículo',
          component: () => import('@/views/reportes/HistorialVehiculo.vue'),
        },
        {
          path: 'reportes/costos-fechas',
          name: 'Reporte Costos entre Fechas',
          component: () => import('@/views/reportes/CostosEntreFechas.vue'),
        },
        {
          path: 'reportes/gastos-proveedor',
          name: 'Reporte Gastos por Proveedor',
          component: () => import('@/views/reportes/GastosPorProveedor.vue'),
        },
        // Usuarios
        {
          path: 'usuarios',
          name: 'Administración de Usuarios',
          component: () => import('@/views/usuarios/GestionarUsuarios.vue'),
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
