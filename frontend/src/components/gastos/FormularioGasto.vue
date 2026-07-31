<!--
  FormularioGasto.vue — Componente reutilizable para gastos.

  Props:
    - modo: 'crear' | 'editar' | 'detalle'
    - gastoInicial: Object (opcional) — datos a precargar en modo editar/detalle

  Emits:
    - guardado — cuando el formulario se envía exitosamente
-->
<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { gastosService, vehiculosService, tiposGastoService, proveedoresService } from '@/services/modules'

const props = defineProps({
  modo: {
    type: String,
    default: 'crear',
    validator: (v) => ['crear', 'editar', 'detalle'].includes(v),
  },
  gastoInicial: {
    type: Object,
    default: null,
  },
  enModal: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['guardado', 'cancelado'])
const router = useRouter()

const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const vehiculosActivos = ref([])
const tiposGasto = ref([])
const proveedores = ref([])
const usarProveedorRegistrado = ref(false)

const formulario = ref({
  fecha: new Date().toISOString().slice(0, 10),
  valor: '',
  vehiculo_id: '',
  tipo_gasto_id: '',
  proveedor_id: null,
  proveedor_manual: '',
  observaciones: '',
})

// Helpers para mostrar en modo detalle
const getNombreVehiculo = (id) => vehiculosActivos.value.find(v => v.id === id)?.placa || `ID: ${id}`
const getNombreTipo = (id) => tiposGasto.value.find(t => t.id === id)?.nombre || `ID: ${id}`
const getNombreProveedor = (id) => {
  if (!id) return '—'
  return proveedores.value.find(p => p.id === id)?.nombre || `ID: ${id}`
}

const formatValor = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(val)

const cargarDependencias = async () => {
  try {
    const [rVeh, rTipos, rProv] = await Promise.all([
      vehiculosService.obtenerTodos(),
      tiposGastoService.obtenerTodos(),
      proveedoresService.obtenerTodos(),
    ])
    vehiculosActivos.value = rVeh.data.filter(v => v.estado)
    tiposGasto.value = rTipos.data
    proveedores.value = rProv.data
  } catch {
    error.value = 'Error al cargar datos de apoyo.'
  }
}

const inicializarFormulario = () => {
  if (props.gastoInicial) {
    formulario.value = { ...props.gastoInicial }
    usarProveedorRegistrado.value = !!props.gastoInicial.proveedor_id
  }
}

const handleSubmit = async () => {
  if (props.modo === 'detalle') return
  error.value = ''
  mensajeExito.value = ''
  cargando.value = true

  const datos = { ...formulario.value }
  if (!usarProveedorRegistrado.value) {
    datos.proveedor_id = null
  } else {
    datos.proveedor_manual = ''
  }

  try {
    if (props.modo === 'crear') {
      await gastosService.crear(datos)
      mensajeExito.value = 'Gasto registrado exitosamente.'
      formulario.value = { fecha: new Date().toISOString().slice(0, 10), valor: '', vehiculo_id: '', tipo_gasto_id: '', proveedor_id: null, proveedor_manual: '', observaciones: '' }
    } else if (props.modo === 'editar') {
      await gastosService.actualizar(props.gastoInicial.id, datos)
      mensajeExito.value = 'Gasto actualizado correctamente.'
    }
    emit('guardado')
    if (!props.enModal) {
      setTimeout(() => router.push('/gastos'), 1500)
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Error al guardar el gasto.'
  } finally {
    cargando.value = false
  }
}

const esReadOnly = props.modo === 'detalle'
const titulo = { crear: 'Crear Gasto', editar: 'Editar Gasto', detalle: 'Detalle del Gasto' }[props.modo]

onMounted(async () => {
  await cargarDependencias()
  inicializarFormulario()
})

watch(() => props.gastoInicial, inicializarFormulario)
</script>

<template>
  <div class="max-w-2xl mx-auto">
    <div class="mb-6 text-center">
      <h2 class="text-2xl font-bold text-gray-800">{{ titulo }}</h2>
      <span
        v-if="modo !== 'crear'"
        class="text-xs font-semibold px-2 py-1 rounded-full mt-2 inline-block"
        :class="{
          'bg-blue-100 text-blue-700': modo === 'editar',
          'bg-gray-100 text-gray-600': modo === 'detalle',
        }"
      >
        {{ modo === 'editar' ? 'Modo edición' : 'Solo lectura' }}
      </span>
    </div>

    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div v-if="mensajeExito" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
        {{ mensajeExito }}
      </div>
      <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
        {{ error }}
      </div>

      <!-- MODO DETALLE: Vista de solo lectura con tarjetas de datos -->
      <div v-if="esReadOnly && gastoInicial" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Vehículo</p>
            <p class="text-sm font-bold text-gray-800">{{ getNombreVehiculo(gastoInicial.vehiculo_id) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Tipo de Gasto</p>
            <p class="text-sm font-bold text-gray-800">{{ getNombreTipo(gastoInicial.tipo_gasto_id) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Fecha</p>
            <p class="text-sm font-bold text-gray-800">{{ gastoInicial.fecha }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Valor</p>
            <p class="text-sm font-bold text-blue-700">{{ formatValor(gastoInicial.valor) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Proveedor</p>
            <p class="text-sm font-bold text-gray-800">
              {{ gastoInicial.proveedor_manual || getNombreProveedor(gastoInicial.proveedor_id) }}
            </p>
          </div>
          <div v-if="gastoInicial.observaciones" class="bg-slate-50 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-1">Observaciones</p>
            <p class="text-sm text-gray-700">{{ gastoInicial.observaciones }}</p>
          </div>
        </div>
        <div class="pt-2">
          <button v-if="enModal" type="button" @click="$emit('cancelado')" class="inline-block px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors">
            Cerrar
          </button>
          <RouterLink v-else to="/gastos" class="inline-block px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors">
            Cerrar
          </RouterLink>
        </div>
      </div>

      <!-- MODO CREAR / EDITAR: Formulario interactivo -->
      <form v-else @submit.prevent="handleSubmit" class="space-y-5">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Vehículo *</label>
            <select v-model="formulario.vehiculo_id" required :disabled="esReadOnly" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500">
              <option value="" disabled>Seleccionar vehículo...</option>
              <option v-for="v in vehiculosActivos" :key="v.id" :value="v.id">{{ v.placa }} - {{ v.marca }}</option>
            </select>
            <p v-if="vehiculosActivos.length === 0 && !esReadOnly" class="text-xs text-orange-500 mt-1">No hay vehículos activos disponibles.</p>
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Tipo de Gasto *</label>
            <select v-model="formulario.tipo_gasto_id" required :disabled="esReadOnly" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500">
              <option value="" disabled>Seleccionar tipo...</option>
              <option v-for="t in tiposGasto" :key="t.id" :value="t.id">{{ t.nombre }}</option>
            </select>
          </div>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Fecha *</label>
            <input type="date" v-model="formulario.fecha" required :readonly="esReadOnly" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 read-only:text-gray-500" />
          </div>
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Valor (COP) *</label>
            <input type="number" v-model.number="formulario.valor" required min="0" :readonly="esReadOnly" placeholder="ej. 150000" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 read-only:text-gray-500" />
          </div>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-2">Proveedor</label>
          <div v-if="!esReadOnly" class="flex gap-4 mb-3">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" :value="false" v-model="usarProveedorRegistrado" />
              <span class="text-sm text-gray-700">Proveedor manual</span>
            </label>
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="radio" :value="true" v-model="usarProveedorRegistrado" />
              <span class="text-sm text-gray-700">Proveedor registrado</span>
            </label>
          </div>
          <input v-if="!usarProveedorRegistrado" v-model="formulario.proveedor_manual" :readonly="esReadOnly" placeholder="ej. Taller El Mecanico" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 read-only:text-gray-500" />
          <select v-else v-model="formulario.proveedor_id" :disabled="esReadOnly" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-50 disabled:text-gray-500">
            <option :value="null">Sin proveedor</option>
            <option v-for="p in proveedores" :key="p.id" :value="p.id">{{ p.nombre }} — {{ p.nit }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Observaciones</label>
          <textarea v-model="formulario.observaciones" rows="3" :readonly="esReadOnly" placeholder="Detalles adicionales..." class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none read-only:bg-gray-50 read-only:text-gray-500"></textarea>
        </div>
        <div v-if="!esReadOnly" class="flex gap-3 pt-2">
          <button
            type="submit"
            :disabled="cargando || vehiculosActivos.length === 0"
            class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white font-bold rounded-lg text-sm shadow-md transition-colors"
          >
            {{ cargando ? 'Guardando...' : (modo === 'editar' ? 'Actualizar Gasto' : 'Registrar Gasto') }}
          </button>
          <button v-if="enModal" type="button" @click="$emit('cancelado')" class="flex-1 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg transition-colors text-sm">
            Cancelar
          </button>
          <RouterLink v-else to="/gastos" class="flex-1 py-2.5 text-center bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors">
            Cancelar
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
