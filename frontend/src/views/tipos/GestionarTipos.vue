<script setup>
import { ref, computed, onMounted } from 'vue'
import { tiposGastoService } from '@/services/modules'

const tiposGasto = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Creación
const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const formularioCreacion = ref({ nombre: '' })

const cargarTipos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await tiposGastoService.obtenerTodos()
    tiposGasto.value = res.data
  } catch {
    error.value = 'Error al cargar los tipos de gasto.'
  } finally {
    cargando.value = false
  }
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = { nombre: '' }
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const crearTipo = async () => {
  errorCrear.value = ''
  creando.value = true
  try {
    await tiposGastoService.crear(formularioCreacion.value)
    mensajeExito.value = '¡Tipo de gasto creado exitosamente!'
    cerrarModalCrear()
    await cargarTipos()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al crear el tipo de gasto.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (tipo) => {
  editando.value = tipo.id
  formularioEdicion.value = { ...tipo }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await tiposGastoService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Tipo de gasto actualizado correctamente.'
    editando.value = null
    await cargarTipos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar.'
  }
}

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.ceil(tiposGasto.value.length / POR_PAGINA))
const tiposPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return tiposGasto.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }

onMounted(cargarTipos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Tipos de Gasto</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Tipo de Gasto
      </button>
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
            <th class="px-4 py-3 w-[75%]">Nombre</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="tiposGasto.length === 0">
            <td colspan="2" class="text-center py-10 text-gray-400">No hay tipos de gasto registrados.</td>
          </tr>
          <tr v-for="t in tiposPaginados" :key="t.id" class="hover:bg-slate-50" v-show="editando !== t.id">
            <td class="px-4 py-3 font-medium text-gray-800">{{ t.nombre }}</td>
            <td class="px-4 py-3">
              <button @click="iniciarEdicion(t)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
              </button>
            </td>
          </tr>
          <tr v-for="t in tiposPaginados" :key="'e-' + t.id" v-show="editando === t.id" class="bg-blue-50 border-l-4 border-blue-500">
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.nombre" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="guardarEdicion(t.id)" title="Guardar" class="text-green-600 hover:text-green-800 transition-colors">
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ tiposGasto.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Tipo de Gasto</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="crearTipo" class="p-6 space-y-4">
          <div v-if="errorCrear" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ errorCrear }}
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
            <input v-model="formularioCreacion.nombre" required placeholder="ej. Gasolina" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" />
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="cerrarModalCrear" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ creando ? 'Guardando...' : 'Crear Tipo' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
