<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center">
    <h1 class="text-3xl font-bold text-gray-800 mb-6">Bienvenido al Panel (Aún en construcción)</h1>
    <button 
      @click="logout"
      class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
    >
      Cerrar sesión
    </button>
  </div>
</template>
