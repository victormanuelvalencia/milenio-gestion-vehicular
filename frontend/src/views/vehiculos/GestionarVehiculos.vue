<script setup>
import { ref, computed, onMounted } from 'vue'
import { vehiculosService } from '@/services/modules'

const vehiculos = ref([])
const cargando = ref(false)
const error = ref('')
const editando = ref(null)
const formularioEdicion = ref({})
const mensajeExito = ref('')
const busqueda = ref('')

const mostrarModalCrear = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const formularioCreacion = ref({ placa: '', marca: '', ano: new Date().getFullYear(), estado: true })

const cargarVehiculos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await vehiculosService.obtenerTodos()
    vehiculos.value = res.data
  } catch {
    error.value = 'Error al cargar los vehículos.'
  } finally {
    cargando.value = false
  }
}

const abrirModalCrear = () => {
  errorCrear.value = ''
  formularioCreacion.value = { placa: '', marca: '', ano: new Date().getFullYear(), estado: true }
  mostrarModalCrear.value = true
}
const cerrarModalCrear = () => { mostrarModalCrear.value = false }

const crearVehiculo = async () => {
  errorCrear.value = ''
  creando.value = true
  try {
    await vehiculosService.crear(formularioCreacion.value)
    mensajeExito.value = '¡Vehículo creado exitosamente!'
    cerrarModalCrear()
    await cargarVehiculos()
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al crear el vehículo.'
  } finally {
    creando.value = false
  }
}

const iniciarEdicion = (v) => { editando.value = v.id; formularioEdicion.value = { ...v } }
const cancelarEdicion = () => { editando.value = null; formularioEdicion.value = {} }

const guardarEdicion = async (id) => {
  error.value = ''; mensajeExito.value = ''
  try {
    await vehiculosService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Vehículo actualizado correctamente.'
    editando.value = null
    await cargarVehiculos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el vehículo.'
  }
}

const cambiarEstado = async (v) => {
  error.value = ''; mensajeExito.value = ''
  try {
    await vehiculosService.actualizar(v.id, { estado: !v.estado })
    mensajeExito.value = `Vehículo ${!v.estado ? 'activado' : 'desactivado'} correctamente.`
    await cargarVehiculos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al cambiar el estado.'
  }
}

const vehiculosFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return vehiculos.value
  return vehiculos.value.filter(v =>
    v.placa?.toLowerCase().includes(q) || v.marca?.toLowerCase().includes(q)
  )
})

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.max(1, Math.ceil(vehiculosFiltrados.value.length / POR_PAGINA)))
const vehiculosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return vehiculosFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }

const resetPagina = () => { paginaActual.value = 1 }

onMounted(cargarVehiculos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Vehículos</h2>
      <button @click="abrirModalCrear" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" /></svg>
        Nuevo Vehículo
      </button>
    </div>

    <!-- Buscador -->
    <div class="mb-4 relative">
      <svg xmlns="http://www.w3.org/2000/svg" class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" /></svg>
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por placa o marca..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
    </div>

    <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex justify-between">
      {{ mensajeExito }}<button @click="mensajeExito = ''" class="font-bold hover:text-green-900">x</button>
    </div>
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex justify-between">
      {{ error }}<button @click="error = ''" class="font-bold hover:text-red-900">x</button>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando vehículos...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <table class="w-full text-sm text-center table-fixed">
        <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
          <tr>
            <th class="px-4 py-3 w-[15%]">Placa</th>
            <th class="px-4 py-3 w-[20%]">Marca</th>
            <th class="px-4 py-3 w-[15%]">Año</th>
            <th class="px-4 py-3 w-[15%]">Estado</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="vehiculosFiltrados.length === 0">
            <td colspan="5" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay vehículos registrados.' }}</td>
          </tr>
          <tr v-for="v in vehiculosPaginados" :key="v.id" class="hover:bg-slate-50 transition-colors" v-show="editando !== v.id">
            <td class="px-4 py-3 font-bold text-gray-800">{{ v.placa }}</td>
            <td class="px-4 py-3 text-gray-700">{{ v.marca }}</td>
            <td class="px-4 py-3 text-gray-700">{{ v.ano }}</td>
            <td class="px-4 py-3">
              <span class="px-2 py-1 rounded-full text-xs font-semibold" :class="v.estado ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'">
                {{ v.estado ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-center gap-3">
                <button @click="iniciarEdicion(v)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                </button>
                <button @click="cambiarEstado(v)" :title="v.estado ? 'Desactivar' : 'Activar'" :class="v.estado ? 'text-orange-500 hover:text-orange-700' : 'text-green-600 hover:text-green-800'" class="transition-colors">
                  <svg v-if="v.estado" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>
                </button>
              </div>
            </td>
          </tr>
          <tr v-for="v in vehiculosPaginados" :key="'edit-' + v.id" v-show="editando === v.id" class="bg-blue-50 border-l-4 border-blue-500">
            <td class="px-4 py-2"><input v-model="formularioEdicion.placa" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model="formularioEdicion.marca" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model.number="formularioEdicion.ano" type="number" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-3"><span class="px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">Editando</span></td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="guardarEdicion(v.id)" title="Guardar" class="text-green-600 hover:text-green-800 transition-colors"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m4.5 12.75 6 6 9-13.5" /></svg></button>
                <button @click="cancelarEdicion" title="Cancelar" class="text-gray-400 hover:text-gray-600 transition-colors"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" /></svg></button>
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
      <button v-for="p in totalPaginas" :key="p" @click="irPagina(p)" class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors border" :class="p === paginaActual ? 'bg-slate-800 text-white border-slate-800' : 'bg-white border-gray-200 text-gray-600 hover:bg-slate-50'">{{ p }}</button>
      <button @click="irPagina(paginaActual + 1)" :disabled="paginaActual === totalPaginas" class="px-3 py-1.5 rounded-lg text-sm font-medium transition-colors disabled:opacity-30 disabled:cursor-not-allowed bg-white border border-gray-200 text-gray-600 hover:bg-slate-50">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4"><path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" /></svg>
      </button>
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ vehiculosFiltrados.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Vehículo</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600"><svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg></button>
        </div>
        <form @submit.prevent="crearVehiculo" class="p-6 space-y-4">
          <div v-if="errorCrear" class="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">{{ errorCrear }}</div>
          <div><label class="block text-sm font-medium text-gray-700 mb-1">Placa *</label><input v-model="formularioCreacion.placa" required placeholder="ej. ABC123" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label><input v-model="formularioCreacion.marca" required placeholder="ej. Chevrolet" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" /></div>
          <div class="grid grid-cols-2 gap-4">
            <div><label class="block text-sm font-medium text-gray-700 mb-1">Año *</label><input v-model.number="formularioCreacion.ano" type="number" required min="1900" :max="new Date().getFullYear() + 1" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" /></div>
            <div><label class="block text-sm font-medium text-gray-700 mb-1">Estado inicial</label><select v-model="formularioCreacion.estado" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"><option :value="true">Activo</option><option :value="false">Inactivo</option></select></div>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="cerrarModalCrear" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50">{{ creando ? 'Guardando...' : 'Crear Vehículo' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
