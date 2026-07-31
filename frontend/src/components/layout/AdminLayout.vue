<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { mantenimientosProgramadosService } from '@/services/modules'

const authStore = useAuthStore()
const menuPerfilAbierto = ref(false)
const panelNotificacionesAbierto = ref(false)
const notificaciones = ref([])
const leidas = ref(new Set(JSON.parse(localStorage.getItem('noti_leidas') || '[]')))

const handleLogout = () => {
  authStore.logout()
}

const toggleMenuPerfil = () => {
  menuPerfilAbierto.value = !menuPerfilAbierto.value
}

const cerrarMenuPerfil = () => {
  menuPerfilAbierto.value = false
}

const togglePanelNotificaciones = () => {
  panelNotificacionesAbierto.value = !panelNotificacionesAbierto.value
  menuPerfilAbierto.value = false
}

const cerrarPanelNotificaciones = () => {
  panelNotificacionesAbierto.value = false
}

// Carga los mantenimientos programados y filtra los que entran en la ventana de 3 días
const cargarNotificaciones = async () => {
  try {
    const res = await mantenimientosProgramadosService.obtenerTodos()
    const hoy = new Date()
    hoy.setHours(0, 0, 0, 0)

    notificaciones.value = res.data.filter(m => {
      // Parsear fecha sin problemas de zona horaria
      const [y, mo, d] = m.fecha_programada.split('-').map(Number)
      const fechaProgramada = new Date(y, mo - 1, d)
      const diffMs = fechaProgramada - hoy
      const diffDias = Math.ceil(diffMs / (1000 * 60 * 60 * 24))
      // Mostrar si faltan 3 días o menos (incluyendo vencidos)
      return diffDias <= 3
    })
  } catch {
    // silencio si no se puede cargar
  }
}

const marcarLeida = (id) => {
  leidas.value.add(id)
  localStorage.setItem('noti_leidas', JSON.stringify([...leidas.value]))
}

const marcarTodasLeidas = () => {
  notificaciones.value.forEach(n => leidas.value.add(n.id))
  localStorage.setItem('noti_leidas', JSON.stringify([...leidas.value]))
}

const notificacionesNoLeidas = computed(() =>
  notificaciones.value.filter(n => !leidas.value.has(n.id))
)

const conteoNoLeidas = computed(() => notificacionesNoLeidas.value.length)

const formatFecha = (f) => {
  if (!f) return '—'
  const [y, m, d] = f.split('-')
  return `${d}/${m}/${y}`
}

const diasRestantes = (fechaStr) => {
  const hoy = new Date()
  hoy.setHours(0, 0, 0, 0)
  const [y, mo, d] = fechaStr.split('-').map(Number)
  const fecha = new Date(y, mo - 1, d)
  const diff = Math.ceil((fecha - hoy) / (1000 * 60 * 60 * 24))
  if (diff < 0) return { texto: `Vencido hace ${Math.abs(diff)} día${Math.abs(diff) !== 1 ? 's' : ''}`, clase: 'text-red-600 font-semibold' }
  if (diff === 0) return { texto: 'Vence hoy', clase: 'text-red-600 font-semibold' }
  if (diff === 1) return { texto: 'Vence mañana', clase: 'text-orange-600 font-semibold' }
  return { texto: `Vence en ${diff} días`, clase: 'text-yellow-600 font-semibold' }
}

// Recarga notificaciones cada 5 minutos
let intervalo = null
onMounted(() => {
  cargarNotificaciones()
  intervalo = setInterval(cargarNotificaciones, 5 * 60 * 1000)
})
onUnmounted(() => {
  if (intervalo) clearInterval(intervalo)
})

const menuPrincipal = [
  { name: 'Vehículos', to: '/vehiculos' },
  { name: 'Conductores', to: '/conductores' },
  { name: 'Viajes', to: '/viajes' },
  { name: 'Mantenimientos', to: '/mantenimientos' },
  { name: 'Programar mantenimientos', to: '/mantenimientos-programados' },
  { name: 'Gastos', to: '/gastos' },
  { name: 'Tipos de gasto', to: '/tipos-gasto' },
  { name: 'Proveedores', to: '/proveedores' }
]
</script>

<template>
  <div class="flex h-screen bg-gray-100 font-sans" @click="cerrarMenuPerfil; cerrarPanelNotificaciones()">

    <!-- Sidebar / Columna Izquierda -->
    <aside class="w-72 bg-slate-800 text-white flex flex-col fixed h-full shadow-xl">

      <div class="p-5 bg-slate-900 flex items-center justify-center">
        <img
          src="/logo.png"
          alt="Logo empresa"
          class="h-50 object-contain"
          onerror="this.style.display='none'; this.nextElementSibling.style.display='block'"
        />
        <span
          class="hidden text-white font-bold text-lg tracking-widest"
          style="display: none;"
        >
          MILENIO
        </span>
      </div>

      <nav class="flex-1 overflow-y-auto py-4">
        <ul class="space-y-2 px-3">
          
          <!-- Enlaces Directos -->
          <li v-for="item in menuPrincipal" :key="item.name">
            <RouterLink
              :to="item.to"
              class="flex items-center px-4 py-3 rounded-lg transition-colors duration-200 text-slate-300 hover:bg-slate-700 w-full"
              active-class="bg-blue-600 text-white shadow-md hover:bg-blue-600"
            >
              <span class="font-medium text-sm">{{ item.name }}</span>
            </RouterLink>
          </li>

          <!-- Link Directo a Reportes y Usuarios -->
          <li class="pt-2 mt-2 border-t border-slate-700/50">
            <RouterLink
              to="/reportes"
              class="flex items-center px-4 py-3 rounded-lg transition-colors duration-200 text-slate-300 hover:bg-slate-700"
              active-class="bg-blue-600 text-white shadow-md hover:bg-blue-600"
            >
              <span class="font-medium text-sm">Reportes</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink
              to="/usuarios"
              class="flex items-center px-4 py-3 rounded-lg transition-colors duration-200 text-slate-300 hover:bg-slate-700"
              active-class="bg-blue-600 text-white shadow-md hover:bg-blue-600"
            >
              <span class="font-medium text-sm">Administración de usuarios</span>
            </RouterLink>
          </li>
          
        </ul>
      </nav>

    </aside>

    <!-- Main Content / Columna Derecha -->
    <main class="flex-1 ml-72 overflow-y-auto bg-slate-50 relative">

      <!-- Top Header -->
      <header class="bg-white shadow-sm sticky top-0 z-10 px-8 py-3 flex justify-end items-center gap-3">

        <!-- Botón de Notificaciones -->
        <div class="relative" @click.stop>
          <button
            id="btn-notificaciones"
            title="Notificaciones de mantenimientos"
            @click="togglePanelNotificaciones"
            class="relative p-2 rounded-full text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
          >
            <!-- Icono campana (SVG) -->
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <!-- Badge contador -->
            <span
              v-if="conteoNoLeidas > 0"
              class="absolute -top-0.5 -right-0.5 min-w-[18px] h-[18px] bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center px-1 leading-none"
            >
              {{ conteoNoLeidas > 9 ? '9+' : conteoNoLeidas }}
            </span>
          </button>

          <!-- Panel de notificaciones desplegable -->
          <div
            v-if="panelNotificacionesAbierto"
            class="absolute right-0 mt-2 w-96 bg-white rounded-xl shadow-xl border border-gray-100 z-50 overflow-hidden"
          >
            <!-- Cabecera del panel -->
            <div class="px-4 py-3 border-b border-gray-100 flex items-center justify-between bg-slate-50">
              <div class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span class="font-semibold text-sm text-slate-700">Mantenimientos próximos</span>
                <span v-if="notificaciones.length > 0" class="text-xs text-slate-400">({{ notificaciones.length }})</span>
              </div>
              <button
                v-if="conteoNoLeidas > 0"
                @click="marcarTodasLeidas"
                class="text-xs text-blue-600 hover:text-blue-800 font-medium transition-colors"
              >
                Marcar todas como leídas
              </button>
            </div>

            <!-- Lista de notificaciones -->
            <div class="max-h-96 overflow-y-auto divide-y divide-gray-50">
              <!-- Sin notificaciones -->
              <div v-if="notificaciones.length === 0" class="px-4 py-8 text-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto text-gray-200 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <p class="text-sm text-gray-400">Sin mantenimientos próximos</p>
                <p class="text-xs text-gray-300 mt-1">Aparecen 3 días antes de la fecha programada</p>
              </div>

              <!-- Cada notificación -->
              <div
                v-for="noti in notificaciones"
                :key="noti.id"
                class="px-4 py-3 transition-colors"
                :class="leidas.has(noti.id) ? 'bg-white' : 'bg-blue-50'"
              >
                <div class="flex items-start gap-3">
                  <!-- Indicador de no leída -->
                  <div class="mt-1.5 flex-shrink-0">
                    <span
                      v-if="!leidas.has(noti.id)"
                      class="block w-2 h-2 bg-blue-500 rounded-full"
                    ></span>
                    <span v-else class="block w-2 h-2 bg-transparent rounded-full"></span>
                  </div>

                  <!-- Contenido -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-0.5">
                      <span class="text-sm font-bold text-slate-800">{{ noti.vehiculo?.placa || '—' }}</span>
                      <span :class="['text-xs', diasRestantes(noti.fecha_programada).clase]">
                        · {{ diasRestantes(noti.fecha_programada).texto }}
                      </span>
                    </div>
                    <p class="text-sm text-gray-600 leading-snug truncate" :title="noti.descripcion">{{ noti.descripcion }}</p>
                    <div class="flex items-center gap-1 mt-1">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      <span class="text-xs text-gray-400">{{ formatFecha(noti.fecha_programada) }}</span>
                    </div>
                  </div>

                  <!-- Acciones -->
                  <div class="flex flex-col gap-1 flex-shrink-0">
                    <RouterLink
                      to="/mantenimientos-programados"
                      @click="cerrarPanelNotificaciones"
                      class="text-xs text-blue-600 hover:text-blue-800 font-medium whitespace-nowrap transition-colors"
                      title="Ver en tabla"
                    >
                      Ver
                    </RouterLink>
                    <button
                      v-if="!leidas.has(noti.id)"
                      @click="marcarLeida(noti.id)"
                      class="text-xs text-gray-400 hover:text-gray-600 transition-colors whitespace-nowrap"
                      title="Marcar como leída"
                    >
                      Leída
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Pie del panel -->
            <div v-if="notificaciones.length > 0" class="px-4 py-2 border-t border-gray-100 bg-slate-50">
              <RouterLink
                to="/mantenimientos-programados"
                @click="cerrarPanelNotificaciones"
                class="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 transition-colors"
              >
                Ver todos los mantenimientos programados
                <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </RouterLink>
            </div>
          </div>
        </div>

        <!-- Botón de Perfil de Usuario -->
        <div class="relative" @click.stop>
          <button
            id="btn-perfil"
            @click="toggleMenuPerfil"
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <!-- Icono usuario (SVG) -->
            <div class="w-8 h-8 bg-slate-700 rounded-full flex items-center justify-center text-white">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <span class="text-sm font-medium">{{ authStore.userNombre }}</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>

          <!-- Menú Desplegable de Perfil -->
          <div
            v-if="menuPerfilAbierto"
            class="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-100 py-1 z-50"
          >
            <div class="px-4 py-2 border-b border-gray-100">
              <p class="text-xs text-gray-400">Sesión activa</p>
              <p class="text-sm font-semibold text-gray-700">{{ authStore.userNombre }}</p>
              <p class="text-xs text-blue-600 font-medium mt-0.5">{{ authStore.userRol }}</p>
            </div>
            <button
              id="btn-cerrar-sesion"
              @click="handleLogout"
              class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors font-medium"
            >
              Cerrar sesión
            </button>
          </div>
        </div>

      </header>

      <!-- Content Area -->
      <div class="p-8">
        <RouterView />
      </div>
    </main>

  </div>
</template>
