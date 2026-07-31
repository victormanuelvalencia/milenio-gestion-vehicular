<script setup>
import { ref, computed, onMounted } from 'vue'
import { mantenimientosService, vehiculosService, proveedoresService } from '@/services/modules'
import FormularioMantenimiento from '@/components/mantenimientos/FormularioMantenimiento.vue'
import SearchableSelect from '@/components/common/SearchableSelect.vue'

const mantenimientos = ref([])
const vehiculos = ref([])
const proveedores = ref([])

const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const editando = ref(null)
const formularioEdicion = ref({})

// Creación
const mostrarModalCrear = ref(false)

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [resMan, resVeh, resProv] = await Promise.all([
      mantenimientosService.obtenerTodos(),
      vehiculosService.obtenerTodos(),
      proveedoresService.obtenerTodos()
    ])
    mantenimientos.value = resMan.data
    vehiculos.value = resVeh.data.filter(v => v.estado)
    proveedores.value = resProv.data
  } catch {
    error.value = 'Error al cargar los datos. Verifica la conexión.'
  } finally {
    cargando.value = false
  }
}

const formatMoneda = (v) => new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(v)
const formatFecha = (f) => {
  if (!f) return '—'
  const partes = f.split('-')
  if (partes.length === 3) return `${partes[2]}/${partes[1]}/${partes[0]}`
  return f
}

const getNombreProveedor = (id) => {
  if (!id) return '—'
  return proveedores.value.find(p => p.id === id)?.nombre || `#${id}`
}

const abrirModalCrear = () => {
  mostrarModalCrear.value = true
}

const cerrarModalCrear = () => {
  mostrarModalCrear.value = false
}

const onMantenimientoGuardado = async () => {
  mensajeExito.value = '¡Mantenimiento registrado exitosamente!'
  cerrarModalCrear()
  await cargarDatos()
}

const editarUsarProveedorRegistrado = ref(false)

const iniciarEdicion = (m) => {
  editando.value = m.id
  formularioEdicion.value = { ...m }
  editarUsarProveedorRegistrado.value = !!m.proveedor_id
}

const cancelarEdicion = () => {
  editando.value = null
  formularioEdicion.value = {}
}

const guardarEdicion = async (id) => {
  error.value = ''
  mensajeExito.value = ''
  
  const datos = { ...formularioEdicion.value }
  if (!editarUsarProveedorRegistrado.value) {
    datos.proveedor_id = null
  } else {
    datos.proveedor_manual = ''
  }

  try {
    await mantenimientosService.actualizar(id, datos)
    mensajeExito.value = 'Mantenimiento actualizado correctamente.'
    editando.value = null
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al actualizar el mantenimiento.'
  }
}

const eliminarMantenimiento = async (m) => {
  if (!confirm(`¿Estás seguro de eliminar el mantenimiento del vehículo ${m.vehiculo?.placa || m.vehiculo_id} por ${formatMoneda(m.valor)}?`)) return
  error.value = ''
  mensajeExito.value = ''
  try {
    await mantenimientosService.eliminar(m.id)
    mensajeExito.value = 'Mantenimiento eliminado correctamente.'
    await cargarDatos()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al eliminar el mantenimiento.'
  }
}

const busqueda = ref('')
const mantenimientosFiltrados = computed(() => {
  const q = busqueda.value.toLowerCase().trim()
  if (!q) return mantenimientos.value
  return mantenimientos.value.filter(m => {
    const placa = (m.vehiculo?.placa || '').toLowerCase()
    const provManual = (m.proveedor_manual || '').toLowerCase()
    const provRegistrado = (getNombreProveedor(m.proveedor_id) || '').toLowerCase()
    const desc = (m.descripcion || '').toLowerCase()
    return placa.includes(q) || provManual.includes(q) || provRegistrado.includes(q) || desc.includes(q)
  })
})

const POR_PAGINA = 10
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.max(1, Math.ceil(mantenimientosFiltrados.value.length / POR_PAGINA)))
const mantenimientosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return mantenimientosFiltrados.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }
const resetPagina = () => { paginaActual.value = 1 }

onMounted(cargarDatos)
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Gestión de Mantenimientos</h2>
      <button
        @click="abrirModalCrear"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium text-sm flex items-center gap-2 transition-colors shadow-sm"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo Mantenimiento
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
      <input v-model="busqueda" @input="resetPagina" type="text" placeholder="Buscar por placa, proveedor o descripción..." class="w-full pl-9 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-sm" />
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando mantenimientos...</div>

    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden border border-gray-100">
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-center">
          <thead class="bg-slate-800 text-white text-xs uppercase tracking-wide">
            <tr>
              <th class="px-3 py-3 w-[10%]">Fecha</th>
              <th class="px-3 py-3 w-[10%]">Placa</th>
              <th class="px-3 py-3 w-[10%]">Kilometraje</th>
              <th class="px-3 py-3 w-[25%]">Descripción</th>
              <th class="px-3 py-3 w-[20%]">Proveedor</th>
              <th class="px-3 py-3 w-[10%]">Valor</th>
              <th class="px-3 py-3 w-[15%]">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-if="mantenimientosFiltrados.length === 0">
              <td colspan="7" class="text-center py-10 text-gray-400">{{ busqueda ? 'Sin resultados para la búsqueda.' : 'No hay mantenimientos registrados.' }}</td>
            </tr>
            <!-- Fila Normal -->
            <tr
              v-for="m in mantenimientosPaginados"
              :key="m.id"
              class="hover:bg-slate-50 transition-colors"
              v-show="editando !== m.id"
            >
              <td class="px-3 py-3 font-medium text-gray-700">{{ formatFecha(m.fecha) }}</td>
              <td class="px-3 py-3 font-bold text-gray-800">{{ m.vehiculo?.placa || '—' }}</td>
              <td class="px-3 py-3 text-gray-600">{{ m.kilometraje.toLocaleString('es-CO') }} km</td>
              <td class="px-3 py-3 text-gray-600 max-w-[150px] truncate" :title="m.descripcion">{{ m.descripcion || '—' }}</td>
              <td class="px-3 py-3 text-gray-600 truncate max-w-[150px]" :title="m.proveedor_manual || getNombreProveedor(m.proveedor_id)">
                {{ m.proveedor_manual || getNombreProveedor(m.proveedor_id) }}
              </td>
              <td class="px-3 py-3 font-semibold text-blue-700">{{ formatMoneda(m.valor) }}</td>
              <td class="px-3 py-3">
                <div class="flex items-center justify-center gap-3">
                  <button @click="iniciarEdicion(m)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                  </button>
                  <button @click="eliminarMantenimiento(m)" title="Eliminar" class="text-red-500 hover:text-red-700 transition-colors">
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
              <td class="px-2 py-2"><input type="date" v-model="formularioEdicion.fecha" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2">
                <SearchableSelect
                  v-model="formularioEdicion.vehiculo_id"
                  :options="vehiculos.map(v => ({ value: v.id, label: v.placa }))"
                />
              </td>
              <td class="px-2 py-2"><input v-model.number="formularioEdicion.kilometraje" type="number" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2"><input v-model="formularioEdicion.descripcion" placeholder="Descripción" class="w-full px-1 py-1 text-xs border rounded" /></td>
              <td class="px-2 py-2">
                <div class="flex gap-2 mb-1 justify-center">
                  <label class="text-[10px] flex items-center gap-1 cursor-pointer"><input type="radio" :value="false" v-model="editarUsarProveedorRegistrado" /> Manual</label>
                  <label class="text-[10px] flex items-center gap-1 cursor-pointer"><input type="radio" :value="true" v-model="editarUsarProveedorRegistrado" /> Registrado</label>
                </div>
                <input v-if="!editarUsarProveedorRegistrado" v-model="formularioEdicion.proveedor_manual" class="w-full px-1 py-1 text-xs border rounded" placeholder="Proveedor manual" />
                <SearchableSelect
                  v-else
                  v-model="formularioEdicion.proveedor_id"
                  :options="[{value: null, label: 'Ninguno'}, ...proveedores.map(p => ({ value: p.id, label: p.nombre }))]"
                />
              </td>
              <td class="px-2 py-2"><input v-model.number="formularioEdicion.valor" type="number" class="w-full px-1 py-1 text-xs border rounded" /></td>
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ mantenimientosFiltrados.length }} registros</span>
    </div>

    <!-- Modal de Creación -->
    <div v-if="mostrarModalCrear" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 overflow-y-auto">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-2xl my-8">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50 sticky top-0 z-10">
          <h3 class="text-lg font-bold text-gray-800">Registrar Mantenimiento</h3>
          <button @click="cerrarModalCrear" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <FormularioMantenimiento @guardado="onMantenimientoGuardado" @cancelado="cerrarModalCrear" />
      </div>
    </div>
  </div>
</template>
