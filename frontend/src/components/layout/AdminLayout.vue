<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const menuPerfilAbierto = ref(false)

const handleLogout = () => {
  authStore.logout()
}

const toggleMenuPerfil = () => {
  menuPerfilAbierto.value = !menuPerfilAbierto.value
}

const cerrarMenuPerfil = () => {
  menuPerfilAbierto.value = false
}

const navLinks = [
  { name: 'Gestionar vehículos', to: '/vehiculos' },
  { name: 'Crear vehículo', to: '/vehiculos/crear' },
  { name: 'Gestionar gastos', to: '/gastos' },
  { name: 'Crear gasto', to: '/gastos/crear' },
  { name: 'Gestionar tipos de gasto', to: '/tipos-gasto' },
  { name: 'Crear tipo de gasto', to: '/tipos-gasto/crear' },
  { name: 'Gestionar proveedores', to: '/proveedores' },
  { name: 'Crear proveedor', to: '/proveedores/crear' },
]
</script>

<template>
  <div class="flex h-screen bg-gray-100 font-sans" @click="cerrarMenuPerfil">

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
        <ul class="space-y-1 px-3">
          <li v-for="link in navLinks" :key="link.name">
            <RouterLink
              :to="link.to"
              class="flex items-center px-4 py-3 rounded-lg transition-colors duration-200 text-slate-300 hover:bg-slate-700"
              active-class="bg-blue-600 text-white shadow-md hover:bg-blue-600"
            >
              <span class="font-medium text-sm">{{ link.name }}</span>
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
        <button
          id="btn-notificaciones"
          title="Notificaciones"
          class="relative p-2 rounded-full text-gray-500 hover:bg-gray-100 hover:text-gray-700 transition-colors"
        >
          <!-- Icono campana (SVG) -->
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>

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
            <span class="text-sm font-medium">Administrador</span>
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
              <p class="text-sm font-semibold text-gray-700">Administrador</p>
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
