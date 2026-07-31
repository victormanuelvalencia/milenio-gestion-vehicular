<script setup>
import { ref, computed, onMounted } from 'vue'
import { mantenimientosProgramadosService, vehiculosService } from '@/services/modules'
import FormularioMantenimiento from '@/components/mantenimientos/FormularioMantenimiento.vue'

const mantenimientosProgramados = ref([])
const vehiculos = ref([])

const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Creación de programación
const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')

const formularioCreacion = ref({
  vehiculo_id: '',
  descripcion: '',
  fecha_programada: new Date().toISOString().slice(0, 10),
})

// Modal para registrar mantenimiento real ("Hecho")
const mostrarModalHecho = ref(false)
const mantenimientoEnProceso = ref(null)

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [resMan, resVeh] = await Promise.all([
      mantenimientosProgramadosService.obtenerTodos(),
      vehiculosService.obtenerTodos()
    ])
    mantenimientosProgramados.value = resMan.data
    vehiculos.value = resVeh.data.filter(v => v.estado)
  } catch {
    error.value = 'Error al cargar los datos. Verifica la conexión.'
  } finally {
    cargando.value = false
  }
}

const formatFecha = (f) => {
  if (!f) return '—'
  const partes = f.split('-')
  if (partes.length === 3) return `${partes[2]}/${partes[1]}/${partes[0]}`
  return f
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = {
    vehiculo_id: '',
    descripcion: '',
    fecha_programada: new Date().toISOString().slice(0, 10),
  }
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const crearMantenimientoProgramado = async () => {
  errorCrear.value = ''
  creando.value = true
  
  try {
    await mantenimientosProgramadosService.crear(formularioCreacion.value)
    mensajeExito.value = '¡Programación guardada exitosamente!'
    cerrarModalCrear()
    await cargarDatos()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al guardar la programación.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (m) => {
  editando.value = m.id
  formularioEdicion.value = { ...m }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await mantenimientosProgramadosService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Programación actualizada correctamente.'
    editando.value = null
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar la programación.'
  }
}

const eliminarMantenimientoProgramado = async (m) => {
  if (!confirm(`¿Estás seguro de eliminar esta programación para el vehículo ${m.vehiculo?.placa || m.vehiculo_id}?`)) return
  error.value = ''
  mensajeExito.value = ''
  try {
    await mantenimientosProgramadosService.eliminar(m.id)
    mensajeExito.value = 'Programación eliminada correctamente.'
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar la programación.'
  }
}

// Flujo "Marcar como hecho"
const abrirModalHecho = (m) => {
  mantenimientoEnProceso.value = m
  mostrarModalHecho.value = true
}

const cerrarModalHecho = () => {
  mostrarModalHecho.value = false
  mantenimientoEnProceso.value = null
}

const onMantenimientoRealizado = async () => {
  try {
    const id = mantenimientoEnProceso.value.id
    // Eliminamos el programado
    await mantenimientosProgramadosService.eliminar(id)
    // Limpiar la marca de "leída" de localStorage para este ID
    const leidas = new Set(JSON.parse(localStorage.getItem('noti_leidas') || '[]'))
    leidas.delete(id)
    localStorage.setItem('noti_leidas', JSON.stringify([...leidas]))
    mensajeExito.value = 'Mantenimiento registrado y eliminado de la programación.'
    cerrarModalHecho()
    await cargarDatos()
  } catch (e) {
    error.value = 'El mantenimiento se registró, pero ocurrió un error al eliminar la programación.'
  }
}

const busqueda = ref('')
const mantenimientosProgramadosFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return mantenimientosProgramados.value
  return mantenimientosProgramados.value.filter(m =>
    m.vehiculo?.placa?.toLowerCase().includes(q) ||
    m.descripcion?.toLowerCase().includes(q) ||
    m.estado?.toLowerCase().includes(q)
  )
})

const POR_PAGINA = 10
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.max(1, Math.ceil(mantenimientosProgramadosFiltrados.value.length / POR_PAGINA)))
const mantenimientosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return mantenimientosProgramadosFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }
const resetPagina = () => { paginaActual.value = 1 }

onMounted(cargarDatos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Programar Mantenimientos</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Programar
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
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por placa, descripción o estado..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando mantenimientos programados...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-center">
          <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
            <tr>
              <th class="px-3 py-3 w-[15%]">Fecha Programada</th>
              <th class="px-3 py-3 w-[15%]">Placa</th>
              <th class="px-3 py-3 w-[40%]">Descripción</th>
              <th class="px-3 py-3 w-[10%]">Estado</th>
              <th class="px-3 py-3 w-[20%]">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="mantenimientosProgramadosFiltrados.length === 0">
              <td colspan="5" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay mantenimientos programados.' }}</td>
            </tr>
            <!-- Fila Normal -->
            <tr
              v-for="m in mantenimientosPaginados"
              :key="m.id"
              class="hover:bg-slate-50 transition-colors"
              v-show="editando !== m.id"
            >
              <td class="px-3 py-3 font-medium text-gray-700">{{ formatFecha(m.fecha_programada) }}</td>
              <td class="px-3 py-3 font-bold text-gray-800">{{ m.vehiculo?.placa || '—' }}</td>
              <td class="px-3 py-3 text-gray-600 text-left">{{ m.descripcion }}</td>
              <td class="px-3 py-3">
                <span class="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs font-semibold rounded-full">{{ m.estado }}</span>
              </td>
              <td class="px-3 py-3">
                <div class="flex items-center justify-center gap-2">
                  <button @click="abrirModalHecho(m)" title="Marcar como Hecho" class="text-emerald-500 hover:text-emerald-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" /></svg>
                  </button>
                  <button @click="iniciarEdicion(m)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                  </button>
                  <button @click="eliminarMantenimientoProgramado(m)" title="Eliminar" class="text-red-500 hover:text-red-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
                  </button>
                </div>
              </td>
            </tr>
            <!-- Fila de Edición Inline -->
            <tr
              v-for="m in mantenimientosPaginados"
              :key="'edit-' + m.id"
              v-show="editando === m.id"
              class="bg-blue-50 border-l-4 border-blue-500"
            >
              <td class="px-2 py-2"><input type="date" v-model="formularioEdicion.fecha_programada" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2">
                <select v-model="formularioEdicion.vehiculo_id" class="w-full px-1 py-1 text-xs border rounded">
                  <option v-for="veh in vehiculos" :key="veh.id" :value="veh.id">{{ veh.placa }}</option>
                </select>
              </td>
              <td class="px-2 py-2"><input v-model="formularioEdicion.descripcion" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2 text-gray-500 text-xs">{{ m.estado }}</td>
              <td class="px-2 py-2">
                <div class="flex justify-center gap-2">
                  <button @click="guardarEdicion(m.id)" title="Guardar" class="text-green-600 hover:text-green-800"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg></button>
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ mantenimientosProgramadosFiltrados.length }} registros</span>
    </div>

    <!-- Modal de Creación Programación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-lg my-8">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <h3 class="text-lg font-bold text-gray-800">Programar Mantenimiento</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="crearMantenimientoProgramado" class="p-6">
          <div v-if="errorCrear" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ errorCrear }}
          </div>
          
          <div class="grid grid-cols-1 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo *</label>
              <select v-model="formularioCreacion.vehiculo_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm">
                <option value="" disabled>Seleccione...</option>
                <option v-for="v in vehiculos" :key="v.id" :value="v.id">{{ v.placa }}</option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Fecha Programada *</label>
              <input type="date" v-model="formularioCreacion.fecha_programada" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Descripción del mantenimiento *</label>
              <textarea v-model="formularioCreacion.descripcion" required rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" placeholder="Ej. Cambio de aceite y filtros..."></textarea>
            </div>
          </div>

          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="cerrarModalCrear" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ creando ? 'Guardando...' : 'Programar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Marcar como Hecho -->
    <div v-if="mostrarModalHecho" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl my-8">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <div>
            <h3 class="text-lg font-bold text-gray-800">Registrar Mantenimiento Realizado</h3>
            <p class="text-xs text-gray-500 mt-0.5">
              Registra los datos reales del mantenimiento programado para <span class="font-semibold">{{ mantenimientoEnProceso?.vehiculo?.placa }}</span>.
            </p>
          </div>
          <button @click="cerrarModalHecho" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        
        <FormularioMantenimiento
          v-if="mantenimientoEnProceso"
          :vehiculoIdInicial="mantenimientoEnProceso.vehiculo_id"
          :descripcionInicial="mantenimientoEnProceso.descripcion"
          @guardado="onMantenimientoRealizado"
          @cancelado="cerrarModalHecho"
        />
      </div>
    </div>
  </div>
</template>
