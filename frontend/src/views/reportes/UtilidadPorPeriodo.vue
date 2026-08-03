<script setup>
import { ref, onMounted, computed } from 'vue'
import { vehiculosService, reportesService } from '@/services/modules'
import SearchableSelect from '@/components/common/SearchableSelect.vue'
import { exportarAExcel, exportarAPDF } from '@/utils/exportUtils'

const vehiculos = ref([])
const filtros = ref({ vehiculo_id: '', fecha_inicio: '', fecha_fin: '' })
const resultados = ref([])
const buscado = ref(false)
const cargando = ref(false)

const totalFletes = computed(() => resultados.value.reduce((s, r) => s + (r.ingresos || 0), 0))
const totalGastos = computed(() => resultados.value.reduce((s, r) => s + (r.gastos || 0), 0))
const totalUtilidad = computed(() => totalFletes.value - totalGastos.value)

const formatValor = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v)

onMounted(async () => {
  const { data } = await vehiculosService.obtenerTodos()
  vehiculos.value = data
})

const buscar = async () => {
  cargando.value = true
  try {
    const params = {}
    if (filtros.value.vehiculo_id) params.vehiculo_id = filtros.value.vehiculo_id
    if (filtros.value.fecha_inicio) params.fecha_inicio = filtros.value.fecha_inicio
    if (filtros.value.fecha_fin) params.fecha_fin = filtros.value.fecha_fin
    const { data } = await reportesService.utilidadPorPeriodo(params)
    resultados.value = data
    buscado.value = true
  } finally {
    cargando.value = false
  }
}

const columnasExportacion = [
  { header: 'Placa', key: 'vehiculo' },
  { header: 'Total Fletes', key: 'ingresos' },
  { header: 'Total Gastos', key: 'gastos' },
  { header: 'Utilidad', key: 'utilidad' },
]

const exportarExcel = () => exportarAExcel(resultados.value, columnasExportacion, 'Utilidad_Periodo')
const exportarPDF = () => exportarAPDF(resultados.value, columnasExportacion, 'Utilidad_Periodo', 'Reporte de Utilidad por Período')
</script>

<template>
  <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Utilidad por Período</h2>
        <p class="text-sm text-slate-500 mt-1">Calcula la utilidad de cada vehículo restando los gastos a los fletes en un rango de fechas.</p>
      </div>
      <div class="flex gap-2">
        <button @click="exportarExcel" class="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 text-white text-sm font-bold rounded-lg transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Exportar Excel
        </button>
        <button @click="exportarPDF" class="flex items-center gap-2 px-4 py-2 bg-red-600 hover:bg-red-700 text-white text-sm font-bold rounded-lg transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
          Exportar PDF
        </button>
      </div>
    </div>

    <!-- Filtros -->
    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo</label>
          <SearchableSelect
            v-model="filtros.vehiculo_id"
            :options="[{value: '', label: 'Todos los vehículos'}, ...vehiculos.map(v => ({ value: v.id, label: v.placa }))]"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Inicial</label>
          <input v-model="filtros.fecha_inicio" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Final</label>
          <input v-model="filtros.fecha_fin" type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
        </div>
        <div>
          <button @click="buscar" :disabled="cargando" class="w-full bg-blue-600 hover:bg-blue-700 disabled:opacity-60 text-white font-bold py-2 px-4 rounded-lg transition-colors text-sm">
            {{ cargando ? 'Buscando...' : 'Buscar' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Resultados -->
    <template v-if="buscado">
      <!-- Tarjetas de resumen (solo si hay más de un vehículo o todos) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div class="p-3 bg-blue-50 text-blue-600 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Total Fletes</p>
            <p class="text-2xl font-bold text-slate-800">{{ formatValor(totalFletes) }}</p>
          </div>
        </div>

        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div class="p-3 bg-red-50 text-red-500 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Total Gastos</p>
            <p class="text-2xl font-bold text-slate-800">{{ formatValor(totalGastos) }}</p>
          </div>
        </div>

        <div class="p-5 rounded-xl shadow-sm border flex items-center gap-4"
          :class="totalUtilidad >= 0 ? 'bg-emerald-50 border-emerald-200' : 'bg-red-50 border-red-200'">
          <div class="p-3 rounded-lg" :class="totalUtilidad >= 0 ? 'bg-emerald-100 text-emerald-600' : 'bg-red-100 text-red-600'">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium" :class="totalUtilidad >= 0 ? 'text-emerald-700' : 'text-red-700'">Utilidad Total</p>
            <p class="text-2xl font-bold" :class="totalUtilidad >= 0 ? 'text-emerald-800' : 'text-red-700'">{{ formatValor(totalUtilidad) }}</p>
          </div>
        </div>
      </div>

      <!-- Tabla -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
        <table class="w-full text-sm text-center table-fixed">
          <thead class="bg-slate-800 text-white text-xs tracking-wide">
            <tr>
              <th class="px-4 py-3 w-[25%]">Placa</th>
              <th class="px-4 py-3 w-[25%]">Total Fletes</th>
              <th class="px-4 py-3 w-[25%]">Total Gastos</th>
              <th class="px-4 py-3 w-[25%]">Utilidad</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="resultados.length === 0">
              <td colspan="4" class="text-center py-10 text-gray-400">No hay resultados para los filtros seleccionados.</td>
            </tr>
            <tr v-for="r in resultados" :key="r.vehiculo" class="hover:bg-slate-50">
              <td class="px-4 py-3 font-bold text-slate-700">{{ r.vehiculo }}</td>
              <td class="px-4 py-3 font-semibold text-blue-700">{{ formatValor(r.ingresos) }}</td>
              <td class="px-4 py-3 font-semibold text-red-600">{{ formatValor(r.gastos) }}</td>
              <td class="px-4 py-3 font-bold" :class="r.utilidad >= 0 ? 'text-emerald-600' : 'text-red-600'">
                {{ formatValor(r.utilidad) }}
              </td>
            </tr>
            <!-- Fila de totales (solo si hay más de un resultado) -->
            <tr v-if="resultados.length > 1" class="bg-slate-100 border-t-2 border-slate-300">
              <td class="px-4 py-3 font-bold text-slate-800 text-left pl-6">TOTALES</td>
              <td class="px-4 py-3 font-bold text-blue-800">{{ formatValor(totalFletes) }}</td>
              <td class="px-4 py-3 font-bold text-red-700">{{ formatValor(totalGastos) }}</td>
              <td class="px-4 py-3 font-bold text-lg" :class="totalUtilidad >= 0 ? 'text-emerald-700' : 'text-red-700'">
                {{ formatValor(totalUtilidad) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
