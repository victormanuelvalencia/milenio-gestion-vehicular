<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const correo = ref('')
const contrasena = ref('')
const errorMsg = ref('')
const loading = ref(false)

const handleLogin = async () => {
  errorMsg.value = ''
  loading.value = true
  
  const result = await authStore.login(correo.value, contrasena.value)
  
  if (!result.success) {
    errorMsg.value = result.message
  }
  
  loading.value = false
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full bg-slate-900 rounded-lg shadow-xl p-8 border border-slate-800">
      <div class="text-center mb-8">
        <img src="/logo.png" alt="Logo" class="h-45 mx-auto mb-4 object-contain" onerror="this.style.display='none'" />
        <p class="text-slate-400 mt-2">Inicia sesión en tu cuenta</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="correo" class="block text-sm font-medium text-slate-300">Correo Electrónico</label>
          <input 
            id="correo" 
            v-model="correo" 
            type="email" 
            required
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="correo@ejemplo.com"
          />
        </div>
        
        <div>
          <label for="contrasena" class="block text-sm font-medium text-slate-300">Contraseña</label>
          <input 
            id="contrasena" 
            v-model="contrasena" 
            type="password" 
            required
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            placeholder="••••••••"
          />
        </div>
        
        <div v-if="errorMsg" class="p-3 rounded-md bg-red-900/50 border border-red-800 text-red-300 text-sm">
          {{ errorMsg }}
        </div>
        
        <button 
          type="submit" 
          :disabled="loading"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
        >
          <span v-if="loading">Iniciando...</span>
          <span v-else>Iniciar Sesión</span>
        </button>
      </form>
    </div>
  </div>
</template>
