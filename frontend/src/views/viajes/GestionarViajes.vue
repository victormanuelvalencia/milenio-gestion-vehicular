<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import { useRouter } from 'vue-router'
import { viajesService, vehiculosService, conductoresService } from '@/services/modules'
import FormularioGasto from '@/components/gastos/FormularioGasto.vue'
import SearchableSelect from '@/components/common/SearchableSelect.vue'

const router = useRouter()
const viajes = ref([])
const vehiculos = ref([])
const conductores = ref([])

const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Modal agregar gasto desde viaje
const mostrarModalGasto = ref(false)
const viajeParaGasto = ref(null)

const abrirModalGasto = (viaje) => {
  viajeParaGasto.value = viaje
  mostrarModalGasto.value = true
}
const cerrarModalGasto = () => {
  mostrarModalGasto.value = false
  viajeParaGasto.value = null
}
const onGastoGuardado = async () => {
  mensajeExito.value = 'Gasto registrado y asociado al viaje correctamente.'
  cerrarModalGasto()
  await cargarDatos()
}

// Creación
const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const formularioCreacion = ref({
  vehiculo_id: '',
  conductor_id: '',
  empresa: '',
  origen: '',
  destino: '',
  numero_manifiesto: '',
  flete: 0,
  anticipo: 0,
  fecha: ''
})

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [resViajes, resVehiculos, resConductores] = await Promise.all([
      viajesService.obtenerTodos(),
      vehiculosService.obtenerTodos(),
      conductoresService.obtenerTodos()
    ])
    viajes.value = resViajes.data
    vehiculos.value = resVehiculos.data.filter(v => v.estado)
    conductores.value = resConductores.data.filter(c => c.estado)
  } catch {
    error.value = 'Error al cargar los datos. Verifica la conexión.'
  } finally {
    cargando.value = false
  }
}

const formatMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v || 0)

const calcularUtilidad = (viaje) => {
  const totalGastos = (viaje.gastos || []).reduce((acc, g) => acc + parseFloat(g.valor || 0), 0)
  return parseFloat(viaje.flete || 0) - totalGastos
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = {
    vehiculo_id: '',
    conductor_id: '',
    empresa: '',
    origen: '',
    destino: '',
    numero_manifiesto: '',
    flete: 0,
    anticipo: 0,
    fecha: ''
  }
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const crearViaje = async () => {
  errorCrear.value = ''
  creando.value = true
  try {
    const datos = { ...formularioCreacion.value }
    if (!datos.fecha) datos.fecha = null
    await viajesService.crear(datos)
    mensajeExito.value = '¡Viaje registrado exitosamente!'
    cerrarModalCrear()
    await cargarDatos()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al registrar el viaje.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (v) => {
  editando.value = v.id
  formularioEdicion.value = { ...v, fecha: v.fecha || '' }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    const datos = { ...formularioEdicion.value }
    if (!datos.fecha) datos.fecha = null
    await viajesService.actualizar(id, datos)
    mensajeExito.value = 'Viaje actualizado correctamente.'
    editando.value = null
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el viaje.'
  }
}

const eliminarViaje = async (viaje) => {
  if (!confirm(`¿Estás seguro de eliminar el viaje con manifiesto "${viaje.numero_manifiesto}"?`)) return
  error.value = ''
  mensajeExito.value = ''
  try {
    await viajesService.eliminar(viaje.id)
    mensajeExito.value = 'Viaje eliminado correctamente.'
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar el viaje.'
  }
}

const verDetalle = (v) => router.push(`/viajes/${v.id}/detalle`)
const verGastos = (v) => router.push(`/viajes/${v.id}/gastos`)

const busqueda = ref('')
const viajesFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return viajes.value
  return viajes.value.filter(v =>
    v.numero_manifiesto?.toLowerCase().includes(q) ||
    v.empresa?.toLowerCase().includes(q) ||
    v.origen?.toLowerCase().includes(q) ||
    v.destino?.toLowerCase().includes(q) ||
    v.vehiculo?.placa?.toLowerCase().includes(q)
  )
})

const POR_PAGINA = 10
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.max(1, Math.ceil(viajesFiltrados.value.length / POR_PAGINA)))
const viajesPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return viajesFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }
const resetPagina = () => { paginaActual.value = 1 }


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })
watch(mensajeExito, (val) => { if (val) setTimeout(() => mensajeExito.value = '', 3000) })
watch(errorCrear, (val) => { if (val) setTimeout(() => errorCrear.value = '', 3000) })

onMounted(cargarDatos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Viajes</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Viaje
      </button>
    </div>

    <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex justify-between">
      {{ mensajeExito }}
      <button @click="mensajeExito = ''" class="font-bold hover:text-green-900">x</button>
    </div>
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex justify-between">
      {{ error }}
      <button @click="error = ''" class="font-bold hover:text-red-900">x</button>
    </div>

    <!-- Buscador -->
    <div class="mb-4 relative">
      <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" /></svg>
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por manifiesto, empresa, ruta o placa..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando viajes...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-center">
          <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
            <tr>
              <th class="px-3 py-3 w-[20%]">Manifiesto</th>
              <th class="px-3 py-3 w-[15%]">Placa</th>
              <th class="px-3 py-3 w-[15%]">Flete</th>
              <th class="px-3 py-3 w-[15%]">Anticipo</th>
              <th class="px-3 py-3 w-[15%]">Utilidad</th>
              <th class="px-3 py-3 w-[20%]">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="viajesFiltrados.length === 0">
              <td colspan="6" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay viajes registrados.' }}</td>
            </tr>
            <!-- Fila Normal -->
            <tr
              v-for="v in viajesPaginados"
              :key="v.id"
              class="hover:bg-slate-50 transition-colors"
              v-show="editando !== v.id"
            >
              <td class="px-3 py-3 font-bold text-gray-800">{{ v.numero_manifiesto }}</td>
              <td class="px-3 py-3 font-medium text-slate-700">{{ v.vehiculo?.placa || '—' }}</td>
              <td class="px-3 py-3 font-semibold text-blue-700">{{ formatMoneda(v.flete) }}</td>
              <td class="px-3 py-3 font-medium text-orange-600">{{ formatMoneda(v.anticipo) }}</td>
              <td class="px-3 py-3 font-semibold" :class="calcularUtilidad(v) >= 0 ? 'text-emerald-600' : 'text-red-600'">
                {{ formatMoneda(calcularUtilidad(v)) }}
              </td>
              <td class="px-3 py-3">
                <div class="flex items-center justify-center gap-1 flex-wrap">
                  <!-- Ver detalles -->
                  <button @click="verDetalle(v)" title="Ver Detalles" class="text-slate-500 hover:text-slate-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" /></svg>
                  </button>
                  <!-- Ver gastos -->
                  <button @click="verGastos(v)" title="Ver Gastos" class="text-violet-500 hover:text-violet-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 14.25l6-6m4.5-3.493V21.75l-3.75-1.5-3.75 1.5-3.75-1.5-3.75 1.5V4.757c0-1.108.806-2.057 1.907-2.185a48.507 48.507 0 0 1 11.186 0c1.1.128 1.907 1.077 1.907 2.185Z" /></svg>
                  </button>
                  <!-- Crear gasto -->
                  <button @click="abrirModalGasto(v)" title="Agregar Gasto" class="text-emerald-500 hover:text-emerald-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
                  </button>
                  <!-- Editar -->
                  <button @click="iniciarEdicion(v)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                  </button>
                  <!-- Eliminar -->
                  <button @click="eliminarViaje(v)" title="Eliminar" class="text-red-500 hover:text-red-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
                  </button>
                </div>
              </td>
            </tr>
            <!-- Fila de Edición Inline -->
            <tr
              v-for="v in viajesPaginados"
              :key="'edit-' + v.id"
              v-show="editando === v.id"
              class="bg-blue-50 border-l-4 border-blue-500"
            >
              <td class="px-2 py-2"><input v-model="formularioEdicion.numero_manifiesto" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2">
                <SearchableSelect
                  v-model="formularioEdicion.vehiculo_id"
                  :options="vehiculos.map(v => ({ value: v.id, label: v.placa }))"
                />
              </td>
              <td class="px-2 py-2"><input v-model.number="formularioEdicion.flete" type="number" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2"><input v-model.number="formularioEdicion.anticipo" type="number" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2"><input v-model="formularioEdicion.fecha" type="date" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2">
                <div class="flex justify-center gap-2">
                  <button @click="guardarEdicion(v.id)" title="Guardar" class="text-green-600 hover:text-green-800"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg></button>
                  <button @click="cancelarEdicion" title="Cancelar" class="text-gray-400 hover:text-gray-600"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" /></svg></button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ viajes.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl my-8">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <h3 class="text-lg font-bold text-gray-800">Registrar Viaje</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="crearViaje" class="p-6">
          <div v-if="errorCrear" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ errorCrear }}
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="col-span-1 md:col-span-2">
              <label class="block text-sm font-medium text-gray-700 mb-1">Número de Manifiesto *</label>
              <input v-model="formularioCreacion.numero_manifiesto" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm font-medium" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha del Viaje *</label>
              <input v-model="formularioCreacion.fecha" type="date" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Empresa *</label>
              <input v-model="formularioCreacion.empresa" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo *</label>
              <SearchableSelect
                v-model="formularioCreacion.vehiculo_id"
                :options="vehiculos.map(v => ({ value: v.id, label: v.placa }))"
                placeholder="Seleccione..."
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Conductor *</label>
              <SearchableSelect
                v-model="formularioCreacion.conductor_id"
                :options="conductores.map(c => ({ value: c.id, label: `${c.nombre} (${c.cedula})` }))"
                placeholder="Seleccione..."
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Origen *</label>
              <input v-model="formularioCreacion.origen" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Destino *</label>
              <input v-model="formularioCreacion.destino" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Valor del Flete *</label>
              <input v-model.number="formularioCreacion.flete" type="number" required min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Anticipo (Opcional)</label>
              <input v-model.number="formularioCreacion.anticipo" type="number" min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>
          </div>

          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="cerrarModalCrear" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ creando ? 'Guardando...' : 'Guardar Viaje' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Agregar Gasto desde Viaje -->
    <div v-if="mostrarModalGasto" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl my-8">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <div>
            <h3 class="text-lg font-bold text-gray-800">Agregar Gasto al Viaje</h3>
            <p class="text-xs text-gray-500 mt-0.5">
              Manifiesto: <span class="font-semibold text-blue-600">{{ viajeParaGasto?.numero_manifiesto }}</span>
              · {{ viajeParaGasto?.origen }} → {{ viajeParaGasto?.destino }}
            </p>
          </div>
          <button @click="cerrarModalGasto" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <div class="p-4 overflow-y-auto max-h-[75vh]">
          <FormularioGasto
            v-if="viajeParaGasto"
            modo="crear"
            :enModal="true"
            :viajeIdInicial="viajeParaGasto.id"
            :numeroManifiestoInicial="viajeParaGasto.numero_manifiesto"
            :fechaInicial="viajeParaGasto.fecha"
            @guardado="onGastoGuardado"
            @cancelado="cerrarModalGasto"
          />
        </div>
      </div>
    </div>
  </div>
</template>
