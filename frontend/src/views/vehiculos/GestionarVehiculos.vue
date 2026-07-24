<script setup>
import { ref, onMounted } from 'vue'
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
            v-for="v in vehiculos"
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
              <div class="flex items-center justify-center gap-2">
                <button
                  @click="iniciarEdicion(v)"
                  class="w-24 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-md transition-colors"
                >
                  Editar
                </button>
                <button
                  @click="cambiarEstado(v)"
                  class="w-24 px-3 py-1.5 text-xs font-bold rounded-md transition-colors text-white"
                  :class="v.estado ? 'bg-orange-500 hover:bg-orange-600' : 'bg-green-600 hover:bg-green-700'"
                >
                  {{ v.estado ? 'Desactivar' : 'Activar' }}
                </button>
              </div>
            </td>
          </tr>
          <!-- Fila de Edición Inline -->
          <tr
            v-for="v in vehiculos"
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
              <div class="flex justify-center gap-2">
                <button @click="guardarEdicion(v.id)" class="w-24 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-bold rounded-md transition-colors">Guardar</button>
                <button @click="cancelarEdicion" class="w-24 px-3 py-1.5 bg-gray-400 hover:bg-gray-500 text-white text-xs font-bold rounded-md transition-colors">Cancelar</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
