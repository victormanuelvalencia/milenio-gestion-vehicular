<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import { useRouter } from 'vue-router'
import { gastosService, vehiculosService, tiposGastoService, proveedoresService } from '@/services/modules'
import FormularioGasto from '@/components/gastos/FormularioGasto.vue'

const router = useRouter()
const gastos = ref([])
const vehiculos = ref([])
const tiposGasto = ref([])
const proveedores = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')

const mostrarModalCrear = ref(false)
const abrirModalCrear = () => { mostrarModalCrear.value = true }
const cerrarModalCrear = () => { mostrarModalCrear.value = false }
const onGastoCreado = async () => {
  cerrarModalCrear()
  mensajeExito.value = 'Gasto registrado exitosamente.'
  await cargarDatos()
}

const busqueda = ref('')

const POR_PAGINA = 15
const paginaActual = ref(1)
const gastosFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return gastos.value
  return gastos.value.filter(g => {
    const manifiesto = g.viaje?.numero_manifiesto?.toLowerCase() || ''
    const tipo = tiposGasto.value.find(t => t.id === g.tipo_gasto_id)?.nombre?.toLowerCase() || ''
    const proveedor = (g.proveedor_manual || proveedores.value.find(p => p.id === g.proveedor_id)?.nombre || '').toLowerCase()
    const obs = (g.observaciones || '').toLowerCase()
    return manifiesto.includes(q) || tipo.includes(q) || proveedor.includes(q) || obs.includes(q)
  })
})
const totalPaginas = computed(() => Math.max(1, Math.ceil(gastosFiltrados.value.length / POR_PAGINA)))
const gastosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return gastosFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }
const resetPagina = () => { paginaActual.value = 1 }

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

const eliminarGasto = async (g) => {
  if (!confirm(`¿Estás seguro de eliminar el gasto por valor de ${formatValor(g.valor)}?`)) return
  try {
    cargando.value = true
    await gastosService.eliminar(g.id)
    mensajeExito.value = 'Gasto eliminado exitosamente.'
    await cargarDatos()
  } catch {
    error.value = 'Error al eliminar el gasto.'
  } finally {
    cargando.value = false
  }
}

const actualizarVerificacion = async (g) => {
  try {
    await gastosService.actualizar(g.id, { verificado_dian: g.verificado_dian })
  } catch (err) {
    error.value = 'Error al actualizar el estado de verificación.'
    g.verificado_dian = !g.verificado_dian // revertir en caso de error
  }
}


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })
watch(mensajeExito, (val) => { if (val) setTimeout(() => mensajeExito.value = '', 3000) })

onMounted(cargarDatos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Gastos</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Gasto
      </button>
    </div>

    <!-- Buscador -->
    <div class="mb-4 relative">
      <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" /></svg>
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por manifiesto, tipo, proveedor u observaciones..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
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
        <thead class="bg-slate-800 text-white text-xs tracking-wide">
          <tr>
            <th class="px-4 py-3 w-[15%]">Fecha</th>
            <th class="px-4 py-3 w-[10%]">Vehículo</th>
            <th class="px-4 py-3 w-[10%]">Gasto</th>
            <th class="px-4 py-3 w-[15%]">Proveedor</th>
            <th class="px-4 py-3 w-[10%]">Valor</th>
            <th class="px-4 py-3 w-[15%]">Observaciones</th>
            <th class="px-4 py-3 w-[8%]">Verificado</th>
            <th class="px-4 py-3 w-[17%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="gastosFiltrados.length === 0">
            <td colspan="7" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay gastos registrados.' }}</td>
          </tr>
          <tr v-for="g in gastosPaginados" :key="g.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-4 py-3 text-gray-600">{{ formatFecha(g.fecha) }}</td>
            <td class="px-4 py-3 font-bold text-gray-800">{{ getNombreVehiculo(g.vehiculo_id) }}</td>
            <td class="px-4 py-3 text-gray-700">{{ getNombreTipo(g.tipo_gasto_id) }}</td>
            <td class="px-4 py-3 text-gray-600">{{ g.proveedor_manual || getNombreProveedor(g.proveedor_id) }}</td>
            <td class="px-4 py-3 font-semibold text-gray-800">{{ formatValor(g.valor) }}</td>
            <td class="px-4 py-3 text-gray-500 max-w-xs truncate">{{ g.observaciones || '—' }}</td>
            <td class="px-4 py-3 text-center">
              <input type="checkbox" v-model="g.verificado_dian" @change="actualizarVerificacion(g)" class="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer" title="Verificado con DIAN" />
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-center gap-3">
                <button
                  @click="verDetalle(g)"
                  title="Ver Detalle"
                  class="text-slate-500 hover:text-slate-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>
                </button>
                <button
                  @click="editarGasto(g)"
                  title="Editar"
                  class="text-blue-500 hover:text-blue-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                </button>
                <button
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

    <!-- Paginación -->
    <div v-if="totalPaginas > 1" class="flex items-center justify-center gap-1 mt-4">
      <button @click="irPagina(paginaActual - 1)" :disabled="paginaActual === 1" class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-600 hover:bg-slate-50">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" /></svg>
      </button>
      <button v-for="p in totalPaginas" :key="p" @click="irPagina(p)"
        class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors border"
        :class="p === paginaActual ? 'bg-slate-800 text-white border-slate-800' : 'bg-white border-gray-200 text-gray-600 hover:bg-slate-50'"
      >{{ p }}</button>
      <button @click="irPagina(paginaActual + 1)" :disabled="paginaActual === totalPaginas" class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-600 hover:bg-slate-50">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" /></svg>
      </button>
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ gastosFiltrados.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Gasto</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <div class="p-6 max-h-[80vh] overflow-y-auto">
          <FormularioGasto modo="crear" :enModal="true" @guardado="onGastoCreado" @cancelado="cerrarModalCrear" />
        </div>
      </div>
    </div>
  </div>
</template>
