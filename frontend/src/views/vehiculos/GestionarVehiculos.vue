<script setup>
import { ref, computed, onMounted } from 'vue'
import { vehiculosService } from '@/services/modules'

const vehiculos = ref([])
const cargando = ref(false)
const error = ref('')
const editando = ref(null)
const formularioEdicion = ref({})
const mensajeExito = ref('')

const cargarVehiculos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await vehiculosService.obtenerTodos()
    vehiculos.value = res.data
  } catch (e) {
    error.value = 'Error al cargar los vehículos.'
  } finally {
    cargando.value = false
  }
}

const iniciarEdicion = (vehiculo) => {
  editando.value = vehiculo.id
  formularioEdicion.value = { ...vehiculo }
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await vehiculosService.actualizar(id, formularioEdicion.value)
    mensajeExito.value = 'Vehículo actualizado correctamente.'
    editando.value = null
    await cargarVehiculos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el vehículo.'
  }
}

const cambiarEstado = async (vehiculo) => {
  error.value = ''
  mensajeExito.value = ''
  try {
    await vehiculosService.actualizar(vehiculo.id, { estado: !vehiculo.estado })
    mensajeExito.value = `Vehículo ${!vehiculo.estado ? 'activado' : 'desactivado'} correctamente.`
    await cargarVehiculos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al cambiar el estado del vehículo.'
  }
}

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.ceil(vehiculos.value.length / POR_PAGINA))
const vehiculosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return vehiculos.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }

onMounted(cargarVehiculos)
</script>

<template>
  <div>
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Vehículos</h2>
    </div>

    <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm flex justify-between">
      {{ mensajeExito }}
      <button @click="mensajeExito = ''" class="font-bold hover:text-green-900">x</button>
    </div>
    <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm flex justify-between">
      {{ error }}
      <button @click="error = ''" class="font-bold hover:text-red-900">x</button>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando vehículos...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <table class="w-full text-sm text-center table-fixed">
        <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
          <tr>
            <th class="px-4 py-3 w-[15%]">Placa</th>
            <th class="px-4 py-3 w-[15%]">Marca</th>
            <th class="px-4 py-3 w-[15%]">Modelo</th>
            <th class="px-4 py-3 w-[15%]">Año</th>
            <th class="px-4 py-3 w-[15%]">Estado</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="vehiculos.length === 0">
            <td colspan="6" class="text-center py-10 text-gray-400">No hay vehículos registrados.</td>
          </tr>
          <!-- Fila Normal -->
          <tr
            v-for="v in vehiculosPaginados"
            :key="v.id"
            class="hover:bg-slate-50 transition-colors"
            v-show="editando !== v.id"
          >
            <td class="px-4 py-3 font-bold text-gray-800">{{ v.placa }}</td>
            <td class="px-4 py-3 text-gray-700">{{ v.marca }}</td>
            <td class="px-4 py-3 text-gray-700">{{ v.modelo }}</td>
            <td class="px-4 py-3 text-gray-700">{{ v.ano }}</td>
            <td class="px-4 py-3">
              <span
                class="px-2 py-1 rounded-full text-xs font-semibold"
                :class="v.estado ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'"
              >
                {{ v.estado ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td class="px-4 py-3">
              <div class="flex items-center justify-center gap-3">
                <button
                  @click="iniciarEdicion(v)"
                  title="Editar"
                  class="text-blue-500 hover:text-blue-700 transition-colors"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                </button>
                <button
                  @click="cambiarEstado(v)"
                  :title="v.estado ? 'Desactivar' : 'Activar'"
                  :class="v.estado ? 'text-orange-500 hover:text-orange-700' : 'text-green-600 hover:text-green-800'"
                  class="transition-colors"
                >
                  <svg v-if="v.estado" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M18.364 18.364A9 9 0 0 0 5.636 5.636m12.728 12.728A9 9 0 0 1 5.636 5.636m12.728 12.728L5.636 5.636" /></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>
                </button>
              </div>
            </td>
          </tr>
          <!-- Fila de Edición Inline -->
          <tr
            v-for="v in vehiculosPaginados"
            :key="'edit-' + v.id"
            v-show="editando === v.id"
            class="bg-blue-50 border-l-4 border-blue-500"
          >
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.placa" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.marca" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-2">
              <input v-model="formularioEdicion.modelo" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-2">
              <input v-model.number="formularioEdicion.ano" type="number" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </td>
            <td class="px-4 py-3">
              <span class="px-2 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-700">Editando</span>
            </td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="guardarEdicion(v.id)" title="Guardar" class="text-green-600 hover:text-green-800 transition-colors">
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ vehiculos.length }} registros</span>
    </div>
  </div>
</template>
