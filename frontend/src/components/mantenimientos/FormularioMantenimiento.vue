<script setup>
import { ref, onMounted } from 'vue'
import { mantenimientosService, vehiculosService, proveedoresService } from '@/services/modules'

const props = defineProps({
  vehiculoIdInicial: {
    type: [Number, String],
    default: null
  },
  descripcionInicial: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['guardado', 'cancelado'])

const vehiculos = ref([])
const proveedores = ref([])
const cargando = ref(false)
const creando = ref(false)
const errorCrear = ref('')
const usarProveedorRegistrado = ref(false)

const formulario = ref({
  fecha: new Date().toISOString().slice(0, 10),
  kilometraje: '',
  vehiculo_id: props.vehiculoIdInicial || '',
  proveedor_id: null,
  proveedor_manual: '',
  descripcion: props.descripcionInicial || '',
  valor: ''
})

const cargarDatos = async () => {
  cargando.value = true
  try {
    const [resVeh, resProv] = await Promise.all([
      vehiculosService.obtenerTodos(),
      proveedoresService.obtenerTodos()
    ])
    vehiculos.value = resVeh.data.filter(v => v.estado)
    proveedores.value = resProv.data
  } catch (e) {
    errorCrear.value = 'Error al cargar dependencias.'
  } finally {
    cargando.value = false
  }
}

const guardar = async () => {
  errorCrear.value = ''
  creando.value = true
  
  const datos = { ...formulario.value }
  if (!usarProveedorRegistrado.value) {
    datos.proveedor_id = null
  } else {
    datos.proveedor_manual = ''
  }

  try {
    await mantenimientosService.crear(datos)
    emit('guardado')
  } catch (e) {
    errorCrear.value = e.response?.data?.detail || 'Error al guardar el mantenimiento.'
  } finally {
    creando.value = false
  }
}

onMounted(cargarDatos)
</script>

<template>
  <form @submit.prevent="guardar" class="p-6 bg-white rounded-xl">
    <div v-if="errorCrear" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
      {{ errorCrear }}
    </div>
    
    <div v-if="cargando" class="text-sm text-gray-500 py-4 text-center">Cargando formulario...</div>
    
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Vehículo *</label>
        <select v-model="formulario.vehiculo_id" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm">
          <option value="" disabled>Seleccione...</option>
          <option v-for="v in vehiculos" :key="v.id" :value="v.id">{{ v.placa }} - {{ v.marca }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Fecha *</label>
        <input type="date" v-model="formulario.fecha" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Kilometraje *</label>
        <input v-model.number="formulario.kilometraje" type="number" required min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Valor (COP) *</label>
        <input v-model.number="formulario.valor" type="number" required min="0" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
      </div>

      <div class="col-span-1 md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
        <textarea v-model="formulario.descripcion" rows="2" placeholder="Detalles del mantenimiento..." class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm"></textarea>
      </div>

      <div class="col-span-1 md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">Proveedor</label>
        <div class="flex gap-4 mb-3">
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" :value="false" v-model="usarProveedorRegistrado" />
            <span class="text-sm text-gray-700">Proveedor manual</span>
          </label>
          <label class="flex items-center gap-2 cursor-pointer">
            <input type="radio" :value="true" v-model="usarProveedorRegistrado" />
            <span class="text-sm text-gray-700">Proveedor registrado</span>
          </label>
        </div>
        <input v-if="!usarProveedorRegistrado" v-model="formulario.proveedor_manual" placeholder="ej. Taller Central" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
        <select v-else v-model="formulario.proveedor_id" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option :value="null">Sin proveedor</option>
          <option v-for="p in proveedores" :key="p.id" :value="p.id">{{ p.nombre }} — {{ p.nit }}</option>
        </select>
      </div>
    </div>

    <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
      <button type="button" @click="$emit('cancelado')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
      <button type="submit" :disabled="creando" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 disabled:opacity-50">
        {{ creando ? 'Guardando...' : 'Guardar Mantenimiento' }}
      </button>
    </div>
  </form>
</template>
