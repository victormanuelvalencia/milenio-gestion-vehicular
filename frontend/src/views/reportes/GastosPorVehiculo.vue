<script setup>
import { ref, onMounted, computed } from 'vue'
import { vehiculosService, reportesService } from '@/services/modules'
import { exportarAExcel, exportarAPDF } from '@/utils/exportUtils'

const vehiculos = ref([])
const filtros = ref({ vehiculo_id: '', fecha_inicio: '', fecha_fin: '' })
const resultados = ref([])
const buscado = ref(false)
const cargando = ref(false)

const totalGastado = computed(() => resultados.value.reduce((s, g) => s + parseFloat(g.valor || 0), 0))
const cantidad = computed(() => resultados.value.length)

const formatFecha = (f) => { if (!f) return '—'; const p = f.split('-'); return p.length===3 ? `${p[2]}/${p[1]}/${p[0]}` : f }
const formatValor = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v)

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
    const { data } = await reportesService.gastosPorVehiculo(params)
    resultados.value = data
    buscado.value = true
  } finally {
    cargando.value = false
  }
}

const columnasExportacion = [
  { header: 'Fecha', key: (f) => formatFecha(f.fecha) },
  { header: 'Vehículo', key: (f) => f.vehiculo?.placa || '—' },
  { header: 'Tipo de Gasto', key: (f) => f.tipo_gasto?.nombre || '—' },
  { header: 'Proveedor', key: (f) => f.proveedor?.nombre || f.proveedor_manual || '—' },
  { header: 'Valor', key: (f) => f.valor },
  { header: 'Observaciones', key: (f) => f.observaciones || '—' }
]

const exportarExcel = () => exportarAExcel(resultados.value, columnasExportacion, 'Gastos_Vehiculo')
const exportarPDF = () => exportarAPDF(resultados.value, columnasExportacion, 'Gastos_Vehiculo', 'Reporte de Gastos por Vehículo')
</script>

<template>
  <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="text-2xl font-bold text-slate-800">Gastos por Vehículo</h2>
        <p class="text-sm text-slate-500 mt-1">Consulta los gastos asociados a un vehículo específico en un rango de fechas.</p>
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

    <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo</label>
          <select v-model="filtros.vehiculo_id" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
            <option value="">Todos los vehículos</option>
            <option v-for="v in vehiculos" :key="v.id" :value="v.id">{{ v.placa }}</option>
          </select>
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

    <template v-if="buscado">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div class="p-3 bg-blue-50 text-blue-600 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Total Gastado</p>
            <p class="text-2xl font-bold text-slate-800">{{ formatValor(totalGastado) }}</p>
          </div>
        </div>
        <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div class="p-3 bg-emerald-50 text-emerald-600 rounded-lg">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>
          </div>
          <div>
            <p class="text-sm font-medium text-gray-500">Cantidad de Registros</p>
            <p class="text-2xl font-bold text-slate-800">{{ cantidad }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
        <table class="w-full text-sm text-center table-fixed">
          <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
            <tr>
              <th class="px-4 py-3 w-[15%]">Fecha</th>
              <th class="px-4 py-3 w-[15%]">Vehículo</th>
              <th class="px-4 py-3 w-[20%]">Tipo de Gasto</th>
              <th class="px-4 py-3 w-[20%]">Proveedor</th>
              <th class="px-4 py-3 w-[15%]">Valor</th>
              <th class="px-4 py-3 w-[15%]">Observaciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="resultados.length === 0">
              <td colspan="6" class="text-center py-10 text-gray-400">No hay resultados para los filtros seleccionados.</td>
            </tr>
            <tr v-for="g in resultados" :key="g.id" class="hover:bg-slate-50">
              <td class="px-4 py-3 text-gray-600">{{ formatFecha(g.fecha) }}</td>
              <td class="px-4 py-3 font-bold text-slate-700">{{ g.vehiculo?.placa || '—' }}</td>
              <td class="px-4 py-3 text-gray-600">{{ g.tipo_gasto?.nombre || '—' }}</td>
              <td class="px-4 py-3 text-blue-600">{{ g.proveedor?.nombre || g.proveedor_manual || '—' }}</td>
              <td class="px-4 py-3 font-semibold text-slate-800">{{ formatValor(g.valor) }}</td>
              <td class="px-4 py-3 text-gray-500">{{ g.observaciones || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
  </div>
</template>
