<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { gastosService, vehiculosService, tiposGastoService, proveedoresService } from '@/services/modules'

const router = useRouter()
const gastos = ref([])
const vehiculos = ref([])
const tiposGasto = ref([])
const proveedores = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')

const getNombreVehiculo = (id) => vehiculos.value.find(v => v.id === id)?.placa || `#${id}`
const getNombreTipo = (id) => tiposGasto.value.find(t => t.id === id)?.nombre || `#${id}`
const getNombreProveedor = (id) => {
  if (!id) return '—'
  return proveedores.value.find(p => p.id === id)?.nombre || `#${id}`
}

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [rGastos, rVeh, rTipos, rProv] = await Promise.all([
      gastosService.obtenerTodos(),
      vehiculosService.obtenerTodos(),
      tiposGastoService.obtenerTodos(),
      proveedoresService.obtenerTodos(),
    ])
    gastos.value = rGastos.data
    vehiculos.value = rVeh.data
    tiposGasto.value = rTipos.data
    proveedores.value = rProv.data
  } catch {
    error.value = 'Error al cargar los gastos.'
  } finally {
    cargando.value = false
  }
}

const formatFecha = (fecha) => {
  if (!fecha) return '—'
  const partes = fecha.split('-')
  if (partes.length === 3) {
    return `${partes[2]}/${partes[1]}/${partes[0]}`
  }
  return fecha
}

const formatValor = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(val)

const verDetalle = (g) => router.push(`/gastos/${g.id}/detalle`)
const editarGasto = (g) => router.push(`/gastos/${g.id}/editar`)

onMounted(cargarDatos)
</script>

<template>
  <div>
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Gastos</h2>
    </div>

    <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex justify-between">
      {{ mensajeExito }}<button @click="mensajeExito = ''" class="font-bold">x</button>
    </div>
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex justify-between">
      {{ error }}<button @click="error = ''" class="font-bold">x</button>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400">Cargando...</div>
    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <table class="w-full text-sm text-center table-fixed">
        <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
          <tr>
            <th class="px-4 py-3 w-[15%]">Fecha</th>
            <th class="px-4 py-3 w-[10%]">Vehículo</th>
            <th class="px-4 py-3 w-[10%]">Gasto</th>
            <th class="px-4 py-3 w-[15%]">Proveedor</th>
            <th class="px-4 py-3 w-[10%]">Valor</th>
            <th class="px-4 py-3 w-[20%]">Observaciones</th>
            <th class="px-4 py-3 w-[20%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="gastos.length === 0">
            <td colspan="7" class="text-center py-10 text-gray-400">No hay gastos registrados.</td>
          </tr>
          <tr v-for="g in gastos" :key="g.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-4 py-3 text-gray-600">{{ formatFecha(g.fecha) }}</td>
            <td class="px-4 py-3 font-bold text-gray-800">{{ getNombreVehiculo(g.vehiculo_id) }}</td>
            <td class="px-4 py-3 text-gray-700">{{ getNombreTipo(g.tipo_gasto_id) }}</td>
            <td class="px-4 py-3 text-gray-600">{{ g.proveedor_manual || getNombreProveedor(g.proveedor_id) }}</td>
            <td class="px-4 py-3 font-semibold text-gray-800">{{ formatValor(g.valor) }}</td>
            <td class="px-4 py-3 text-gray-500 max-w-xs truncate">{{ g.observaciones || '—' }}</td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-center gap-2">
                <button
                  @click="verDetalle(g)"
                  class="w-24 px-3 py-1.5 bg-slate-600 hover:bg-slate-700 text-white text-xs font-bold rounded-md transition-colors"
                >
                  Detalle
                </button>
                <button
                  @click="editarGasto(g)"
                  class="w-24 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-md transition-colors"
                >
                  Editar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
