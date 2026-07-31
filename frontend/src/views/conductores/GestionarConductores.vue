<script setup>
import { ref, computed, onMounted , watch } from 'vue'
import { conductoresService } from '@/services/modules'

const conductores = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Creación
const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const formularioCreacion = ref({ nombre: '', cedula: '', estado: true })

const cargarConductores = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await conductoresService.obtenerTodos()
    conductores.value = res.data
  } catch {
    error.value = 'Error al cargar los conductores.'
  } finally {
    cargando.value = false
  }
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = { nombre: '', cedula: '', estado: true }
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const crearConductor = async () => {
  errorCrear.value = ''
  creando.value = true
  try {
    await conductoresService.crear(formularioCreacion.value)
    mensajeExito.value = '¡Conductor creado exitosamente!'
    cerrarModalCrear()
    await cargarConductores()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al crear el conductor. Verifica los datos.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (c) => {
  editando.value = c.id
  formularioEdicion.value = { ...c }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await conductoresService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Conductor actualizado correctamente.'
    editando.value = null
    await cargarConductores()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el conductor.'
  }
}

const cambiarEstado = async (conductor) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await conductoresService.actualizar(conductor.id, { estado: !conductor.estado })
    mensajeExito.value = `Conductor ${!conductor.estado ? 'activado' : 'desactivado'} correctamente.`
    await cargarConductores()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al cambiar el estado del conductor.'
  }
}

const eliminarConductor = async (conductor) => {
  if (!confirm(`¿Estás seguro de eliminar al conductor "${conductor.nombre}"?`)) return
  error.value = ''
  mensajeExito.value = ''
  try {
    await conductoresService.eliminar(conductor.id)
    mensajeExito.value = 'Conductor eliminado correctamente.'
    await cargarConductores()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar el conductor.'
  }
}

const busqueda = ref('')
const conductoresFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return conductores.value
  return conductores.value.filter(c =>
    c.nombre?.toLowerCase().includes(q) || c.cedula?.toLowerCase().includes(q)
  )
})

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.max(1, Math.ceil(conductoresFiltrados.value.length / POR_PAGINA)))
const conductoresPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return conductoresFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }
const resetPagina = () => { paginaActual.value = 1 }


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })
watch(mensajeExito, (val) => { if (val) setTimeout(() => mensajeExito.value = '', 3000) })
watch(errorCrear, (val) => { if (val) setTimeout(() => errorCrear.value = '', 3000) })

onMounted(cargarConductores)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Conductores</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Conductor
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
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por nombre o cédula..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando conductores...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <table class="w-full text-sm text-center table-fixed">
        <thead class="bg-slate-800 text-white text-xs tracking-wide">
          <tr>
            <th class="px-4 py-3 w-[30%]">Nombre</th>
            <th class="px-4 py-3 w-[25%]">Cédula</th>
            <th class="px-4 py-3 w-[20%]">Estado</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="conductoresFiltrados.length === 0">
            <td colspan="4" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay conductores registrados.' }}</td>
          </tr>
          <!-- Fila Normal -->
          <tr
            v-for="c in conductoresPaginados"
            :key="c.id"
            class="hover:bg-slate-50 transition-colors"
            v-show="editando !== c.id"
          >
            <td class="px-4 py-3 font-medium text-gray-800">{{ c.nombre }}</td>
            <td class="px-4 py-3 text-gray-700 font-mono">{{ c.cedula }}</td>
            <td class="px-4 py-3">
              <span
                class="px-2 py-1 rounded-full text-xs font-semibold"
                :class="c.estado ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
              >
                {{ c.estado ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-center gap-3">
                <button
                  @click="iniciarEdicion(c)"
                  title="Editar"
                  class="text-blue-500 hover:text-blue-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                </button>
                <button
                  @click="cambiarEstado(c)"
                  :title="c.estado ? 'Desactivar' : 'Activar'"
                  :class="c.estado ? 'text-orange-500 hover:text-orange-700' : 'text-green-600 hover:text-green-800'"
                  class="transition-colors"
                >
                  <svg v-if="c.estado" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>
                </button>
                <button
                  @click="eliminarConductor(c)"
                  title="Eliminar"
                  class="text-red-500 hover:text-red-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
                </button>
              </div>
            </td>
          </tr>
          <!-- Fila de Edición Inline -->
          <tr
            v-for="c in conductoresPaginados"
            :key="'edit-' + c.id"
            v-show="editando === c.id"
            class="bg-blue-50 border-l-4 border-blue-500"
          >
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.nombre" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.cedula" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-3">
              <span class="px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">Editando</span>
            </td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="guardarEdicion(c.id)" title="Guardar" class="text-green-600 hover:text-green-800 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg>
                </button>
                <button @click="cancelarEdicion" title="Cancelar" class="text-gray-400 hover:text-gray-600 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" /></svg>
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ conductoresFiltrados.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Conductor</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="crearConductor" class="p-6 space-y-4">
          <div v-if="errorCrear" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ errorCrear }}
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="formularioCreacion.nombre" required placeholder="ej. Juan Pérez" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cédula *</label>
            <input v-model="formularioCreacion.cedula" required placeholder="ej. 1234567890" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Estado inicial</label>
            <select v-model="formularioCreacion.estado" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
              <option :value="true">Activo</option>
              <option :value="false">Inactivo</option>
            </select>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="cerrarModalCrear" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ creando ? 'Guardando...' : 'Crear Conductor' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
