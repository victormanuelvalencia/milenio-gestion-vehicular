<script setup>
import { ref, computed, onMounted } from 'vue'
import { proveedoresService } from '@/services/modules'

const proveedores = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Creación
const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const formularioCreacion = ref({ nombre: '', nit: '', direccion: '' })

const cargarProveedores = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await proveedoresService.obtenerTodos()
    proveedores.value = res.data
  } catch {
    error.value = 'Error al cargar los proveedores.'
  } finally {
    cargando.value = false
  }
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = { nombre: '', nit: '', direccion: '' }
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const crearProveedor = async () => {
  errorCrear.value = ''
  creando.value = true
  try {
    await proveedoresService.crear(formularioCreacion.value)
    mensajeExito.value = '¡Proveedor creado exitosamente!'
    cerrarModalCrear()
    await cargarProveedores()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al crear el proveedor.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (p) => {
  editando.value = p.id
  formularioEdicion.value = { ...p }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await proveedoresService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Proveedor actualizado correctamente.'
    editando.value = null
    await cargarProveedores()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el proveedor.'
  }
}

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.ceil(proveedores.value.length / POR_PAGINA))
const proveedoresPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return proveedores.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }

onMounted(cargarProveedores)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Proveedores</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Proveedor
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
            <th class="px-4 py-3 w-[25%]">Nombre</th>
            <th class="px-4 py-3 w-[25%]">NIT</th>
            <th class="px-4 py-3 w-[25%]">Dirección</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="proveedores.length === 0">
            <td colspan="4" class="text-center py-10 text-gray-400">No hay proveedores registrados.</td>
          </tr>
          <!-- Fila Normal -->
          <tr v-for="p in proveedoresPaginados" :key="p.id" class="hover:bg-slate-50" v-show="editando !== p.id">
            <td class="px-4 py-3 font-medium text-gray-800">{{ p.nombre }}</td>
            <td class="px-4 py-3 text-gray-700 font-mono">{{ p.nit }}</td>
            <td class="px-4 py-3 text-gray-600">{{ p.direccion || '—' }}</td>
            <td class="px-4 py-3">
              <button @click="iniciarEdicion(p)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
              </button>
            </td>
          </tr>
          <!-- Fila Edición Inline -->
          <tr v-for="p in proveedoresPaginados" :key="'e-' + p.id" v-show="editando === p.id" class="bg-blue-50 border-l-4 border-blue-500">
            <td class="px-4 py-2"><input v-model="formularioEdicion.nombre" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model="formularioEdicion.nit" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model="formularioEdicion.direccion" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="guardarEdicion(p.id)" title="Guardar" class="text-green-600 hover:text-green-800 transition-colors">
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ proveedores.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden flex flex-col max-h-full">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Proveedor</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto">
          <div v-if="errorCrear" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
            {{ errorCrear }}
          </div>
          
          <form @submit.prevent="crearProveedor" class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Nombre *</label>
              <input v-model="formularioCreacion.nombre" required placeholder="ej. Estación El Progreso" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">NIT *</label>
              <input v-model="formularioCreacion.nit" required placeholder="ej. 900123456-1" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-1">Dirección</label>
              <input v-model="formularioCreacion.direccion" placeholder="ej. Cra 10 #20-30" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            
            <div class="flex gap-3 pt-4 border-t border-gray-100 mt-6">
              <button type="button" @click="cerrarModalCrear" class="flex-1 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold rounded-lg transition-colors text-sm">
                Cancelar
              </button>
              <button type="submit" :disabled="creando" class="flex-1 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-semibold rounded-lg transition-colors text-sm shadow-sm">
                {{ creando ? 'Guardando...' : 'Crear Proveedor' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
