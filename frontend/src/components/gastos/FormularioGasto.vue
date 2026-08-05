<!--
  FormularioGasto.vue — Componente reutilizable para gastos.

  Props:
    - modo: 'crear' | 'editar' | 'detalle'
    - gastoInicial: Object (opcional) — datos a precargar en modo editar/detalle
    - enModal: Boolean — si se muestra dentro de un modal
    - viajeIdInicial: Number (opcional) — preselecciona un viaje al abrir desde la tabla de Viajes
    - numeroManifiestoInicial: String (opcional) — muestra el manifiesto como campo readonly
    - fechaInicial: String (opcional) — establece la fecha como readonly (heredada del viaje)

  Emits:
    - guardado — cuando el formulario se envía exitosamente
    - cancelado — cuando el usuario cancela
-->
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { gastosService, tiposGastoService, proveedoresService, viajesService } from '@/services/modules'
import SearchableSelect from '@/components/common/SearchableSelect.vue'

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
  },
  viajeIdInicial: {
    type: Number,
    default: null
  },
  numeroManifiestoInicial: {
    type: String,
    default: null
  },
  fechaInicial: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['guardado', 'cancelado'])
const router = useRouter()

const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')
const tiposGasto = ref([])
const proveedores = ref([])
const viajes = ref([])
const usarProveedorRegistrado = ref(false)

// Cuando viene desde un viaje, el manifiesto y fecha son readonly
const desdeViaje = computed(() => !!props.numeroManifiestoInicial)

const formulario = ref({
  fecha: props.fechaInicial || new Date().toISOString().slice(0, 10),
  valor: '',
  viaje_id: null,
  tipo_gasto_id: '',
  proveedor_id: null,
  proveedor_manual: '',
  observaciones: '',
})

// El viaje seleccionado actualmente
const viajeSeleccionado = computed(() =>
  viajes.value.find(v => v.id === formulario.value.viaje_id) || null
)

// Helpers para mostrar en modo detalle
const getNombreTipo = (id) => tiposGasto.value.find(t => t.id === id)?.nombre || `ID: ${id}`
const getNombreProveedor = (id) => {
  if (!id) return '—'
  return proveedores.value.find(p => p.id === id)?.nombre || `ID: ${id}`
}
const getViajeInfo = (id) => {
  if (!id) return '—'
  const v = viajes.value.find(v => v.id === id)
  if (!v) return `ID: ${id}`
  return `${v.numero_manifiesto}`
}

const formatValor = (val) =>
  new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(val)

const formatearFecha = (f) => {
  if (!f) return '—'
  const dateStr = typeof f === 'string' ? f.split('T')[0] : f
  const p = dateStr.split('-')
  return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : f
}

const cargarDependencias = async () => {
  try {
    const [rTipos, rProv, rViajes] = await Promise.all([
      tiposGastoService.obtenerTodos(),
      proveedoresService.obtenerTodos(),
      viajesService.obtenerTodos()
    ])
    tiposGasto.value = rTipos.data
    proveedores.value = rProv.data
    viajes.value = rViajes.data
  } catch {
    error.value = 'Error al cargar datos de apoyo.'
  }
}

const inicializarFormulario = () => {
  if (props.gastoInicial) {
    formulario.value = { ...props.gastoInicial }
    usarProveedorRegistrado.value = !!props.gastoInicial.proveedor_id
  } else if (props.viajeIdInicial) {
    formulario.value.viaje_id = props.viajeIdInicial
    if (props.fechaInicial) {
      formulario.value.fecha = props.fechaInicial
    }
  }
}

const formularioVacio = () => ({
  fecha: props.fechaInicial || new Date().toISOString().slice(0, 10),
  valor: '',
  viaje_id: props.viajeIdInicial || null,
  tipo_gasto_id: '',
  proveedor_id: null,
  proveedor_manual: '',
  observaciones: '',
})

const handleSubmit = async () => {
  if (props.modo === 'detalle') return
  error.value = ''
  mensajeExito.value = ''
  cargando.value = true

  const datos = { ...formulario.value }

  // Limpiar campo de proveedor no usado
  if (!usarProveedorRegistrado.value) {
    datos.proveedor_id = null
  } else {
    datos.proveedor_manual = ''
  }

  try {
    if (props.modo === 'crear') {
      await gastosService.crear(datos)
      mensajeExito.value = 'Gasto registrado exitosamente.'
      formulario.value = formularioVacio()
      usarProveedorRegistrado.value = false
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
const titulo = { crear: '', editar: 'Editar Gasto', detalle: 'Detalle del Gasto' }[props.modo]


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })
watch(mensajeExito, (val) => { if (val) setTimeout(() => mensajeExito.value = '', 3000) })

onMounted(async () => {
  await cargarDependencias()
  inicializarFormulario()
})

watch(() => props.gastoInicial, inicializarFormulario)
watch(() => props.viajeIdInicial, (nuevoId) => {
  if (nuevoId && props.modo === 'crear') {
    formulario.value.viaje_id = nuevoId
  }
})
watch(() => props.fechaInicial, (nuevaFecha) => {
  if (nuevaFecha && props.modo === 'crear') {
    formulario.value.fecha = nuevaFecha
  }
})
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

      <!-- MODO DETALLE: Vista de solo lectura -->
      <div v-if="esReadOnly && gastoInicial" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <!-- Viaje / Manifiesto -->
          <div class="bg-blue-50 border border-blue-100 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-blue-400 tracking-wide mb-1">Manifiesto</p>
            <p class="text-sm font-bold text-blue-800">{{ getViajeInfo(gastoInicial.viaje_id) }}</p>
            <p v-if="gastoInicial.vehiculo_id || gastoInicial.vehiculo" class="text-xs text-blue-600 mt-1">
              <span class="font-semibold">
                {{ gastoInicial.vehiculo?.placa || `ID ${gastoInicial.vehiculo_id}` }}
              </span>
            </p>
          </div>

          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Tipo de Gasto</p>
            <p class="text-sm font-bold text-gray-800">{{ getNombreTipo(gastoInicial.tipo_gasto_id) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Fecha</p>
            <p class="text-sm font-bold text-gray-800">{{ formatearFecha(gastoInicial.fecha) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Valor</p>
            <p class="text-sm font-bold text-blue-700">{{ formatValor(gastoInicial.valor) }}</p>
          </div>
          <div class="bg-slate-50 rounded-lg p-4">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Proveedor</p>
            <p class="text-sm font-bold text-gray-800">
              {{ gastoInicial.proveedor_manual || getNombreProveedor(gastoInicial.proveedor_id) }}
            </p>
          </div>
          <div v-if="gastoInicial.observaciones" class="bg-slate-50 rounded-lg p-4 col-span-2">
            <p class="text-xs font-semibold text-gray-400 tracking-wide mb-1">Observaciones</p>
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

        <!-- Si viene desde un viaje: mostrar manifiesto y fecha como readonly -->
        <div v-if="desdeViaje" class="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
          <p class="text-xs font-semibold text-blue-500 tracking-wide">Datos del Viaje (solo lectura)</p>
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-semibold text-gray-500 mb-1">Número de Manifiesto</label>
              <input
                :value="numeroManifiestoInicial"
                readonly
                class="w-full px-3 py-2 border border-blue-200 rounded-lg text-sm bg-white text-blue-800 font-bold cursor-not-allowed"
              />
            </div>
            <div>
              <label class="block text-xs font-semibold text-gray-500 mb-1">Fecha del Viaje</label>
              <input
                :value="fechaInicial || '—'"
                readonly
                class="w-full px-3 py-2 border border-blue-200 rounded-lg text-sm bg-white text-blue-800 font-bold cursor-not-allowed"
              />
            </div>
          </div>
        </div>

        <!-- Selector de Manifiesto (solo si NO viene desde un viaje) -->
        <div v-else>
          <label class="block text-sm font-semibold text-gray-700 mb-1">
            Número de Manifiesto (Viaje) *
          </label>
          <SearchableSelect
            v-model="formulario.viaje_id"
            :options="viajes.map(v => ({ value: v.id, label: `${v.numero_manifiesto} — ${v.origen} → ${v.destino}` }))"
            placeholder="Seleccionar manifiesto..."
            :disabled="esReadOnly"
            required
          />
          <p v-if="viajes.length === 0 && !esReadOnly" class="text-xs text-orange-500 mt-1">
            No hay viajes registrados.
          </p>
        </div>

        <!-- Vehículo derivado automáticamente (solo lectura informativa) -->
        <div v-if="viajeSeleccionado && !desdeViaje" class="flex items-center gap-3 px-4 py-2.5 bg-blue-50 border border-blue-100 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-400 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm text-blue-700">
            Vehículo asociado:
            <span class="font-bold">{{ viajeSeleccionado.vehiculo?.placa || '—' }}</span>
          </p>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold text-gray-700 mb-1">Tipo de Gasto *</label>
            <SearchableSelect
              v-model="formulario.tipo_gasto_id"
              :options="tiposGasto.map(t => ({ value: t.id, label: t.nombre }))"
              placeholder="Seleccionar tipo..."
              :disabled="esReadOnly"
              required
            />
          </div>
          <!-- Fecha: solo visible si NO viene de un viaje -->
          <div v-if="!desdeViaje">
            <label class="block text-sm font-semibold text-gray-700 mb-1">Fecha *</label>
            <input type="date" v-model="formulario.fecha" required :readonly="esReadOnly" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 read-only:text-gray-500" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Valor (COP) *</label>
          <input type="number" v-model.number="formulario.valor" required min="0" :readonly="esReadOnly" placeholder="ej. 150000" class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 read-only:bg-gray-50 read-only:text-gray-500" />
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
          <SearchableSelect
            v-else
            v-model="formulario.proveedor_id"
            :options="[{value: null, label: 'Sin proveedor'}, ...proveedores.map(p => ({ value: p.id, label: `${p.nombre} — ${p.nit}` }))]"
            placeholder="Seleccionar proveedor..."
            :disabled="esReadOnly"
          />
        </div>

        <div>
          <label class="block text-sm font-semibold text-gray-700 mb-1">Observaciones</label>
          <textarea v-model="formulario.observaciones" rows="3" :readonly="esReadOnly" placeholder="Detalles adicionales..." class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none read-only:bg-gray-50 read-only:text-gray-500"></textarea>
        </div>

        <div v-if="!esReadOnly" class="flex gap-3 pt-2">
          <button
            type="submit"
            :disabled="cargando || (!formulario.viaje_id && !desdeViaje)"
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
