<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { viajesService, tiposGastoService, proveedoresService, gastosService } from '@/services/modules'
import { usePermisos } from '@/composables/usePermisos'

const { puedeEscribir } = usePermisos()
const route = useRoute()
const router = useRouter()

const viaje = ref(null)
const gastos = ref([])
const tiposGasto = ref([])
const proveedores = ref([])
const cargando = ref(true)
const error = ref('')
const mensajeExito = ref('')

const formatMoneda = (v) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v || 0)

const formatFecha = (fecha) => {
  if (!fecha) return '—'
  const partes = fecha.split('-')
  if (partes.length === 3) return `${partes[2]}/${partes[1]}/${partes[0]}`
  return fecha
}

const getNombreTipo = (id) => tiposGasto.value.find(t => t.id === id)?.nombre || `#${id}`
const getNombreProveedor = (id) => {
  if (!id) return '—'
  return proveedores.value.find(p => p.id === id)?.nombre || `#${id}`
}

const totalGastos = computed(() =>
  gastos.value.reduce((acc, g) => acc + parseFloat(g.valor || 0), 0)
)

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [resViaje, resGastos, rTipos, rProv] = await Promise.all([
      viajesService.obtenerPorId(route.params.id),
      viajesService.obtenerGastos(route.params.id),
      tiposGastoService.obtenerTodos(),
      proveedoresService.obtenerTodos(),
    ])
    viaje.value = resViaje.data
    gastos.value = resGastos.data
    tiposGasto.value = rTipos.data
    proveedores.value = rProv.data
  } catch {
    error.value = 'No se pudieron cargar los gastos del viaje.'
  } finally {
    cargando.value = false
  }
}

}

const editarGasto = (g) => router.push(`/gastos/${g.id}/editar`)

const eliminarGasto = async (g) => {
  if (!confirm(`¿Estás seguro de eliminar el gasto por valor de ${formatMoneda(g.valor)}?`)) return
  try {
    cargando.value = true
    await gastosService.eliminar(g.id)
    mensajeExito.value = 'Gasto eliminado exitosamente.'
    await cargarDatos()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al eliminar el gasto.'
  } finally {
    cargando.value = false
  }
}

watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })
watch(mensajeExito, (val) => { if (val) setTimeout(() => mensajeExito.value = '', 3000) })

onMounted(cargarDatos)
</script>

<template>
  <div>
    <!-- Encabezado -->
    <div class="mb-6 flex items-center gap-3">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">Gastos del Viaje</h2>
        <p v-if="viaje" class="text-sm text-gray-500 mt-0.5">
          Manifiesto <span class="font-semibold text-blue-600">{{ viaje.numero_manifiesto }}</span>
          · {{ viaje.origen }} → {{ viaje.destino }}
        </p>
      </div>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando gastos...</div>
    
    <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex justify-between">
      {{ mensajeExito }}<button @click="mensajeExito = ''" class="font-bold">x</button>
    </div>
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex justify-between">
      {{ error }}<button @click="error = ''" class="font-bold">x</button>
    </div>

    <div v-if="!cargando && error === 'No se pudieron cargar los gastos del viaje.'">
      <!-- Error general ocultando la tabla si falla cargar -->
    </div>
    <div v-else-if="!cargando">
      <!-- Tabla de gastos -->
      <div class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
        <div class="overflow-x-auto">
          <table class="w-full text-sm text-center table-fixed">
            <thead class="bg-slate-800 text-white text-xs tracking-wide">
              <tr>
                <th class="px-4 py-3 w-[15%]">Fecha</th>
                <th class="px-4 py-3 w-[15%]">Tipo de Gasto</th>
                <th class="px-4 py-3 w-[18%]">Proveedor</th>
                <th class="px-4 py-3 w-[12%]">Valor</th>
                <th class="px-4 py-3 w-[25%]">Observaciones</th>
                <th class="px-4 py-3 w-[15%]">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="gastos.length === 0">
                <td colspan="6" class="text-center py-10 text-gray-400">
                  Este viaje no tiene gastos registrados.
                </td>
              </tr>
              <tr v-for="g in gastos" :key="g.id" class="hover:bg-slate-50 transition-colors">
                <td class="px-4 py-3 text-gray-600">{{ formatFecha(g.fecha) }}</td>
                <td class="px-4 py-3 text-gray-700">{{ getNombreTipo(g.tipo_gasto_id) }}</td>
                <td class="px-4 py-3 text-gray-600">{{ g.proveedor_manual || getNombreProveedor(g.proveedor_id) }}</td>
                <td class="px-4 py-3 font-semibold text-gray-800">{{ formatMoneda(g.valor) }}</td>
                <td class="px-4 py-3 text-gray-500 truncate max-w-0">{{ g.observaciones || '—' }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center justify-center gap-3">
                    <button
                      @click="router.push(`/gastos/${g.id}/detalle`)"
                      title="Ver Detalle"
                      class="text-slate-500 hover:text-slate-700 transition-colors"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                      </svg>
                    </button>
                    <button
                      v-if="puedeEscribir"
                      @click="editarGasto(g)"
                      title="Editar"
                      class="text-blue-500 hover:text-blue-700 transition-colors"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                    </button>
                    <button
                      v-if="puedeEscribir"
                      @click="eliminarGasto(g)"
                      title="Eliminar"
                      class="text-red-500 hover:text-red-700 transition-colors"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Resumen financiero debajo de la tabla -->
      <div v-if="viaje && gastos.length > 0" class="mt-4 grid grid-cols-3 gap-3">
        <div class="bg-blue-50 border border-blue-100 rounded-lg p-3 text-center">
          <p class="text-xs text-blue-400 font-semibold tracking-wide">Flete</p>
          <p class="text-base font-bold text-blue-700">{{ formatMoneda(viaje.flete) }}</p>
        </div>
        <div class="bg-red-50 border border-red-100 rounded-lg p-3 text-center">
          <p class="text-xs text-red-400 font-semibold tracking-wide">Total Gastos</p>
          <p class="text-base font-bold text-red-600">{{ formatMoneda(totalGastos) }}</p>
        </div>
        <div
          class="rounded-lg p-3 text-center border"
          :class="(viaje.flete - totalGastos) >= 0 ? 'bg-emerald-50 border-emerald-100' : 'bg-red-50 border-red-100'"
        >
          <p class="text-xs font-semibold tracking-wide"
             :class="(viaje.flete - totalGastos) >= 0 ? 'text-emerald-400' : 'text-red-400'">
            Utilidad
          </p>
          <p class="text-base font-bold" :class="(viaje.flete - totalGastos) >= 0 ? 'text-emerald-600' : 'text-red-600'">
            {{ formatMoneda(viaje.flete - totalGastos) }}
          </p>
        </div>
      </div>

      <!-- Botón volver -->
      <div class="mt-4">
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
