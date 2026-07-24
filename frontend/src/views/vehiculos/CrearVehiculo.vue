<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { vehiculosService } from '@/services/modules'

const router = useRouter()
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')

const formulario = ref({
  placa: '',
  marca: '',
  modelo: '',
  ano: new Date().getFullYear(),
  estado: true,
})

const handleSubmit = async () => {
  error.value = ''
  mensajeExito.value = ''
  cargando.value = true
  try {
    await vehiculosService.crear(formulario.value)
    mensajeExito.value = '¡Vehículo creado exitosamente!'
    formulario.value = { placa: '', marca: '', modelo: '', ano: new Date().getFullYear(), estado: true }
    setTimeout(() => router.push('/vehiculos'), 1500)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al crear el vehículo. Verifica los datos.'
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <div class="max-w-xl mx-auto">
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Crear Vehículo</h2>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
        {{ mensajeExito }}
      </div>
      <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
        {{ error }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-5">
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Placa *</label>
          <input
            v-model="formulario.placa"
            required
            placeholder="ej. ABC123"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Marca *</label>
          <input
            v-model="formulario.marca"
            required
            placeholder="ej. Chevrolet"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Modelo *</label>
          <input
            v-model="formulario.modelo"
            required
            placeholder="ej. FRR"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Año *</label>
          <input
            v-model.number="formulario.ano"
            type="number"
            required
            min="1900"
            :max="new Date().getFullYear() + 1"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Estado inicial</label>
          <div class="flex gap-4">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" :value="true" v-model="formulario.estado" class="text-blue-600" />
              <span class="text-sm text-gray-700">Activo</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" :value="false" v-model="formulario.estado" class="text-blue-600" />
              <span class="text-sm text-gray-700">Inactivo</span>
            </label>
          </div>
        </div>
        <div class="flex gap-3 pt-2">
          <button
            type="submit"
            :disabled="cargando"
            class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold rounded-lg transition-colors text-sm shadow-md"
          >
            {{ cargando ? 'Guardando...' : 'Guardar Vehículo' }}
          </button>
          <RouterLink to="/vehiculos" class="flex-1 py-2.5 text-center bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg transition-colors text-sm">
            Cancelar
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
