<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { viajesService, vehiculosService, conductoresService, empresasService } from '@/services/modules'
import SearchableSelect from '@/components/common/SearchableSelect.vue'
import { usePermisos } from '@/composables/usePermisos'

const { puedeEscribir } = usePermisos()
const route = useRoute()
const router = useRouter()

const vehiculos = ref([])
const conductores = ref([])
const empresas = ref([])

const cargando = ref(true)
const guardando = ref(false)
const error = ref('')

const formulario = ref({
  numero_manifiesto: '',
  fecha: '',
  empresa_id: '',
  vehiculo_id: '',
  conductor_id: '',
  origen: '',
  destino: '',
  flete: 0,
  anticipo: 0
})

const cargarDatos = async () => {
  cargando.value = true
  error.value = ''
  try {
    const [resViaje, resVehiculos, resConductores, resEmpresas] = await Promise.all([
      viajesService.obtenerPorId(route.params.id),
      vehiculosService.obtenerTodos(),
      conductoresService.obtenerTodos(),
      empresasService.obtenerTodos()
    ])
    
    vehiculos.value = resVehiculos.data.filter(v => v.estado || v.id === resViaje.data.vehiculo_id)
    conductores.value = resConductores.data.filter(c => c.estado || c.id === resViaje.data.conductor_id)
    empresas.value = resEmpresas.data

    const v = resViaje.data
    formulario.value = {
      numero_manifiesto: v.numero_manifiesto,
      fecha: v.fecha || '',
      empresa_id: v.empresa_id,
      vehiculo_id: v.vehiculo_id,
      conductor_id: v.conductor_id,
      origen: v.origen,
      destino: v.destino,
      flete: v.flete,
      anticipo: v.anticipo
    }
  } catch (e) {
    error.value = 'Error al cargar los datos del viaje. Verifica tu conexión.'
  } finally {
    cargando.value = false
  }
}

const guardarCambios = async () => {
  guardando.value = true
  error.value = ''
  try {
    const datos = { ...formulario.value }
    if (!datos.fecha) datos.fecha = null
    await viajesService.actualizar(route.params.id, datos)
    router.push('/viajes')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar los cambios.'
    guardando.value = false
  }
}

const cancelar = () => {
  router.push('/viajes')
}

onMounted(() => {
  if (!puedeEscribir) {
    router.push('/viajes')
    return
  }
  cargarDatos()
})
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold text-gray-800">Editar Viaje</h2>
        <p class="text-gray-500 text-sm mt-1">Modifica todos los detalles del viaje seleccionado</p>
      </div>
      <button @click="cancelar" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
        Volver
      </button>
    </div>

    <div v-if="cargando" class="text-center py-16 text-gray-400 text-lg">Cargando datos del viaje...</div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <form @submit.prevent="guardarCambios" class="p-6">
        <div v-if="error" class="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded-r-lg text-sm flex justify-between">
          {{ error }}
          <button type="button" @click="error = ''" class="font-bold hover:text-red-900">x</button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="col-span-1 md:col-span-2">
            <label class="block text-sm font-semibold text-gray-700 mb-1">Número de Manifiesto *</label>
            <input v-model="formulario.numero_manifiesto" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm font-medium" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Fecha del Viaje *</label>
            <input v-model="formulario.fecha" type="date" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Empresa *</label>
            <SearchableSelect
              v-model="formulario.empresa_id"
              :options="empresas.map(e => ({ value: e.id, label: e.nombre }))"
              placeholder="Seleccione..."
              required
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Vehículo *</label>
            <SearchableSelect
              v-model="formulario.vehiculo_id"
              :options="vehiculos.map(v => ({ value: v.id, label: v.placa }))"
              placeholder="Seleccione..."
              required
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Conductor *</label>
            <SearchableSelect
              v-model="formulario.conductor_id"
              :options="conductores.map(c => ({ value: c.id, label: c.nombre }))"
              placeholder="Seleccione..."
              required
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Origen *</label>
            <input v-model="formulario.origen" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Destino *</label>
            <input v-model="formulario.destino" required class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm" />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Valor del Flete *</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium">$</span>
              <input v-model.number="formulario.flete" type="number" required min="0" class="w-full pl-7 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm font-medium text-blue-800" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Anticipo *</label>
            <div class="relative">
              <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500 font-medium">$</span>
              <input v-model.number="formulario.anticipo" type="number" min="0" class="w-full pl-7 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 text-sm font-medium text-orange-700" />
            </div>
          </div>
        </div>

        <div class="pt-6 flex justify-end gap-3 border-t border-gray-100 mt-8">
          <button type="button" @click="cancelar" class="px-5 py-2.5 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
            Cancelar
          </button>
          <button type="submit" :disabled="guardando" class="px-5 py-2.5 text-sm font-semibold text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50">
            {{ guardando ? 'Guardando...' : 'Guardar Cambios' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
