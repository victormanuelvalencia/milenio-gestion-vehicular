<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { tiposGastoService } from '@/services/modules'

const router = useRouter()
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const formulario = ref({ nombre: '' })

const handleSubmit = async () => {
  error.value = ''
  mensajeExito.value = ''
  cargando.value = true
  try {
    await tiposGastoService.crear(formulario.value)
    mensajeExito.value = '¡Tipo de gasto creado exitosamente!'
    formulario.value = { nombre: '' }
    setTimeout(() => router.push('/tipos-gasto'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear el tipo de gasto.'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Crear Tipo de Gasto</h2>
    </div>
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">{{ mensajeExito }}</div>
      <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">{{ error }}</div>
      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Nombre *</label>
          <input v-model="formulario.nombre" required placeholder="ej. Gasolina" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        </div>
        <div class="flex gap-3 pt-2">
          <button type="submit" :disabled="cargando" class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold rounded-lg text-sm shadow-md">
            {{ cargando ? 'Guardando...' : 'Guardar' }}
          </button>
          <RouterLink to="/tipos-gasto" class="flex-1 py-2.5 text-center bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm">Cancelar</RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
