<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { viajesService } from '@/services/modules'

const route = useRoute()
const router = useRouter()
const viaje = ref(null)
const cargando = ref(true)
const error = ref('')

const formatMoneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v || 0)

const formatFecha = (fecha) => {
  if (!fecha) return '—'
  const partes = fecha.split('-')
  if (partes.length === 3) return `${partes[2]}/${partes[1]}/${partes[0]}`
  return fecha
}

const utilidad = computed(() => {
  if (!viaje.value) return 0
  const totalGastos = (viaje.value.gastos || []).reduce((acc, g) => acc + parseFloat(g.valor || 0), 0)
  return parseFloat(viaje.value.flete || 0) - totalGastos
})

onMounted(async () => {
  try {
    const res = await viajesService.obtenerPorId(route.params.id)
    viaje.value = res.data
  } catch {
    error.value = 'No se pudo cargar el viaje.'
  } finally {
    cargando.value = false
  }
})
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <!-- Encabezado -->
    <div class="mb-6 flex items-center gap-3">
      <button @click="router.back()" class="p-2 rounded-lg border border-gray-200 text-gray-500 hover:bg-gray-50 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
        </svg>
      </button>
      <div>
        <h2 class="text-2xl font-bold text-gray-800">Detalle del Viaje</h2>
        <p class="text-sm text-gray-500 mt-0.5">Vista completa del registro — solo lectura</p>
      </div>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando viaje...</div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">{{ error }}</div>

    <div v-else-if="viaje" class="space-y-4">
      <!-- Bloque identificación -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-4">Identificación</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-blue-50 border border-blue-100 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-1">Número de Manifiesto</p>
            <p class="text-xl font-bold text-blue-800">{{ viaje.numero_manifiesto }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Fecha</p>
            <p class="text-sm font-bold text-gray-800">{{ formatFecha(viaje.fecha) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Empresa</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.empresa }}</p>
          </div>
        </div>
      </div>

      <!-- Bloque ruta y asignación -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-4">Ruta y Asignación</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Origen</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.origen }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Destino</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.destino }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Vehículo</p>
            <p class="text-sm font-bold text-gray-800">
              {{ viaje.vehiculo?.placa || '—' }}
              <span v-if="viaje.vehiculo?.marca" class="text-gray-500 font-normal"> — {{ viaje.vehiculo.marca }}</span>
            </p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Conductor</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.conductor?.nombre || '—' }}</p>
            <p v-if="viaje.conductor?.cedula" class="text-xs text-gray-500 mt-0.5">CC: {{ viaje.conductor.cedula }}</p>
          </div>
        </div>
      </div>

      <!-- Bloque financiero -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-4">Información Financiera</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-blue-50 border border-blue-100 rounded-lg p-4">
            <p class="text-xs font-semibold text-blue-400 uppercase tracking-wide mb-1">Flete</p>
            <p class="text-lg font-bold text-blue-700">{{ formatMoneda(viaje.flete) }}</p>
          </div>
          <div class="bg-orange-50 border border-orange-100 rounded-lg p-4">
            <p class="text-xs font-semibold text-orange-400 uppercase tracking-wide mb-1">Anticipo</p>
            <p class="text-lg font-bold text-orange-600">{{ formatMoneda(viaje.anticipo) }}</p>
          </div>
          <div
            class="rounded-lg p-4 border"
            :class="utilidad >= 0 ? 'bg-emerald-50 border-emerald-100' : 'bg-red-50 border-red-100'"
          >
            <p class="text-xs font-semibold uppercase tracking-wide mb-1"
               :class="utilidad >= 0 ? 'text-emerald-400' : 'text-red-400'">
              Utilidad
            </p>
            <p class="text-lg font-bold" :class="utilidad >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ formatMoneda(utilidad) }}
            </p>
            <p class="text-xs mt-1" :class="utilidad >= 0 ? 'text-emerald-500' : 'text-red-400'">
              Flete − Total gastos
            </p>
          </div>
        </div>
      </div>

      <!-- Resumen de gastos -->
      <div v-if="viaje.gastos && viaje.gastos.length > 0" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex justify-between items-center mb-3">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wide">
            Gastos asociados ({{ viaje.gastos.length }})
          </h3>
          <button
            @click="router.push(`/viajes/${viaje.id}/gastos`)"
            class="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors"
          >
            Ver todos los gastos →
          </button>
        </div>
        <p class="text-sm text-gray-500">
          Total de gastos:
          <span class="font-bold text-gray-800">
            {{ formatMoneda(viaje.gastos.reduce((acc, g) => acc + parseFloat(g.valor || 0), 0)) }}
          </span>
        </p>
      </div>
      <div v-else class="bg-slate-50 rounded-xl border border-gray-100 p-4 text-sm text-gray-400 text-center">
        Este viaje no tiene gastos registrados.
      </div>

      <!-- Acciones -->
      <div class="flex gap-3 pt-2">
        <button
          @click="router.push(`/viajes/${viaje.id}/gastos`)"
          class="px-4 py-2 text-sm font-medium text-violet-700 bg-violet-50 border border-violet-200 rounded-lg hover:bg-violet-100 transition-colors"
        >
          Ver Gastos
        </button>
        <button
          @click="router.back()"
          class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
        >
          Volver
        </button>
      </div>
    </div>
  </div>
</template>
