<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { viajesService, tiposGastoService, proveedoresService } from '@/services/modules'

const route = useRoute()
const router = useRouter()

const viaje = ref(null)
const gastos = ref([])
const tiposGasto = ref([])
const proveedores = ref([])
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


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })

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
    <div v-else-if="error" class="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl">{{ error }}</div>

    <div v-else>
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
                <th class="px-4 py-3 w-[8%]">DIAN</th>
                <th class="px-4 py-3 w-[7%]"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-if="gastos.length === 0">
                <td colspan="7" class="text-center py-10 text-gray-400">
                  Este viaje no tiene gastos registrados.
                </td>
              </tr>
              <tr v-for="g in gastos" :key="g.id" class="hover:bg-slate-50 transition-colors">
                <td class="px-4 py-3 text-gray-600">{{ formatFecha(g.fecha) }}</td>
                <td class="px-4 py-3 text-gray-700">{{ getNombreTipo(g.tipo_gasto_id) }}</td>
                <td class="px-4 py-3 text-gray-600">{{ g.proveedor_manual || getNombreProveedor(g.proveedor_id) }}</td>
                <td class="px-4 py-3 font-semibold text-gray-800">{{ formatMoneda(g.valor) }}</td>
                <td class="px-4 py-3 text-gray-500 truncate max-w-0">{{ g.observaciones || '—' }}</td>
                <td class="px-4 py-3 text-center">
                  <span
                    class="inline-block w-2 h-2 rounded-full"
                    :class="g.verificado_dian ? 'bg-emerald-400' : 'bg-gray-300'"
                    :title="g.verificado_dian ? 'Verificado DIAN' : 'Sin verificar'"
                  ></span>
                </td>
                <td class="px-4 py-3">
                  <button
                    @click="router.push(`/gastos/${g.id}/detalle`)"
                    title="Ver detalle del gasto"
                    class="text-slate-400 hover:text-slate-600 transition-colors"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    </svg>
                  </button>
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
