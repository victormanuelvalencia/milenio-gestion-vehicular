<script setup>
import { ref, computed, onMounted , watch } from 'vue'
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


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })

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
  <div class="max-w-2xl mx-auto">
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Detalle del Viaje</h2>
      <span class="text-xs font-semibold px-2 py-1 rounded-full mt-2 inline-block bg-gray-100 text-gray-600">
        Solo lectura
      </span>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando viaje...</div>
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">{{ error }}</div>

    <div v-else-if="viaje" class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <!-- Viaje / Manifiesto -->
          <div class="bg-blue-50 border border-blue-100 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-blue-400 tracking-wide mb-1">Manifiesto</p>
            <p class="text-sm font-bold text-blue-800">{{ viaje.numero_manifiesto }}</p>
            <p class="text-xs text-blue-600 mt-1">
              <span class="font-semibold">{{ viaje.origen }} → {{ viaje.destino }}</span>
            </p>
          </div>

          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Fecha</p>
            <p class="text-sm font-bold text-gray-800">{{ formatFecha(viaje.fecha) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Empresa</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.empresa }}</p>
          </div>
          
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Vehículo</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.vehiculo?.placa || '—' }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Conductor</p>
            <p class="text-sm font-bold text-gray-800">{{ viaje.conductor?.nombre || '—' }}</p>
          </div>

          <!-- Finanzas -->
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Flete</p>
            <p class="text-sm font-bold text-blue-700">{{ formatMoneda(viaje.flete) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Anticipo</p>
            <p class="text-sm font-bold text-orange-600">{{ formatMoneda(viaje.anticipo) }}</p>
          </div>

          <!-- Gastos -->
          <div class="bg-slate-50 rounded-lg p-4 col-span-2 flex justify-between items-center">
            <div>
              <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Total de Gastos ({{ viaje.gastos?.length || 0 }})</p>
              <p class="text-sm font-bold text-gray-800">
                {{ formatMoneda((viaje.gastos || []).reduce((acc, g) => acc + parseFloat(g.valor || 0), 0)) }}
              </p>
            </div>
            <button
              @click="router.push(`/viajes/${viaje.id}/gastos`)"
              class="text-xs font-semibold text-blue-600 hover:text-blue-800 transition-colors"
            >
              Ver Gastos →
            </button>
          </div>

          <div class="bg-slate-50 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Utilidad (Flete - Gastos)</p>
            <p class="text-sm font-bold" :class="utilidad >= 0 ? 'text-emerald-600' : 'text-red-600'">
              {{ formatMoneda(utilidad) }}
            </p>
          </div>
        </div>
        
        <div class="pt-2">
          <button
            @click="router.back()"
            class="inline-block px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors"
          >
            Cerrar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
