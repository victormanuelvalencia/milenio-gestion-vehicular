<script setup>
import { ref, onMounted } from 'vue'
import { proveedoresService } from '@/services/modules'

const proveedores = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

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

onMounted(cargarProveedores)
</script>

<template>
  <div>
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Proveedores</h2>
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
          <tr v-for="p in proveedores" :key="p.id" class="hover:bg-slate-50" v-show="editando !== p.id">
            <td class="px-4 py-3 font-medium text-gray-800">{{ p.nombre }}</td>
            <td class="px-4 py-3 text-gray-700 font-mono">{{ p.nit }}</td>
            <td class="px-4 py-3 text-gray-600">{{ p.direccion || '—' }}</td>
            <td class="px-4 py-3">
              <button @click="iniciarEdicion(p)" class="w-24 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-md">Editar</button>
            </td>
          </tr>
          <!-- Fila Edición Inline -->
          <tr v-for="p in proveedores" :key="'e-' + p.id" v-show="editando === p.id" class="bg-blue-50 border-l-4 border-blue-500">
            <td class="px-4 py-2"><input v-model="formularioEdicion.nombre" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model="formularioEdicion.nit" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-2"><input v-model="formularioEdicion.direccion" class="w-full px-2 py-1.5 border border-blue-300 rounded-md text-sm text-center focus:outline-none focus:ring-2 focus:ring-blue-500" /></td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-2">
                <button @click="guardarEdicion(p.id)" class="w-24 px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white text-xs font-bold rounded-md">Guardar</button>
                <button @click="cancelarEdicion" class="w-24 px-3 py-1.5 bg-gray-400 hover:bg-gray-500 text-white text-xs font-bold rounded-md">Cancelar</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
