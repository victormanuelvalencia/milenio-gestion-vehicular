<!--
  FormularioGastosMasivos.vue — Registro múltiple de gastos para un viaje.

  Props:
    - viaje: Object — objeto del viaje (id, numero_manifiesto, fecha, origen, destino)
    - enModal: Boolean — si se muestra dentro de un modal

  Emits:
    - guardado(gastosCreados) — lista de gastos registrados
    - cancelado
-->
<script setup>
import { ref, computed, onMounted } from 'vue'
import { tiposGastoService, proveedoresService, viajesService } from '@/services/modules'

const props = defineProps({
  viaje: {
    type: Object,
    required: true,
  },
  enModal: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['guardado', 'cancelado'])

// Estado
const cargando = ref(false)
const error = ref('')
const tiposGasto = ref([])
const proveedores = ref([])

// Lista dinámica de filas
const crearFilaVacia = () => ({
  _id: Math.random().toString(36).slice(2),
  tipo_gasto_id: '',
  valor: '',
  usarProveedorRegistrado: false,
  proveedor_id: null,
  proveedor_manual: '',
  observaciones: '',
  errorTipo: false,
  errorValor: false,
})

const filas = ref([crearFilaVacia()])

// Cálculos reactivos 
const totalGastos = computed(() =>
  filas.value.reduce((sum, f) => sum + (parseFloat(f.valor) || 0), 0)
)

const cantidadGastos = computed(() => filas.value.length)

const textoBoton = computed(() => {
  const n = cantidadGastos.value
  return `Registrar ${n} ${n === 1 ? 'gasto' : 'gastos'}`
})

// Utilidades de formato
const formatMoneda = (v) =>
  new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
  }).format(v || 0)

const formatearFecha = (f) => {
  if (!f) return '—'
  const dateStr = typeof f === 'string' ? f.split('T')[0] : f
  const p = dateStr.split('-')
  return p.length === 3 ? `${p[2]}/${p[1]}/${p[0]}` : f
}

// Gestión de filas
const agregarFila = () => filas.value.push(crearFilaVacia())

const eliminarFila = (index) => {
  if (filas.value.length > 1) {
    filas.value.splice(index, 1)
  }
}

// Validación
const validar = () => {
  let valido = true
  filas.value.forEach((f) => {
    f.errorTipo = !f.tipo_gasto_id
    f.errorValor = !f.valor || parseFloat(f.valor) <= 0
    if (f.errorTipo || f.errorValor) valido = false
  })
  return valido
}

// Envío
const handleSubmit = async () => {
  error.value = ''
  if (!validar()) {
    error.value = 'Corrige los campos marcados antes de continuar.'
    return
  }

  cargando.value = true
  try {
    const payload = {
      gastos: filas.value.map((f) => ({
        tipo_gasto_id: parseInt(f.tipo_gasto_id),
        valor: parseFloat(f.valor),
        proveedor_id: f.usarProveedorRegistrado ? (f.proveedor_id || null) : null,
        proveedor_manual: !f.usarProveedorRegistrado ? (f.proveedor_manual || null) : null,
        observaciones: f.observaciones || null,
      })),
    }
    const res = await viajesService.crearGastosMasivos(props.viaje.id, payload)
    emit('guardado', res.data)
  } catch (e) {
    error.value =
      e.response?.data?.detail ||
      'Error al registrar los gastos. Ningún gasto fue guardado.'
  } finally {
    cargando.value = false
  }
}

// Carga de dependencias
onMounted(async () => {
  try {
    const [rTipos, rProv] = await Promise.all([
      tiposGastoService.obtenerTodos(),
      proveedoresService.obtenerTodos(),
    ])
    tiposGasto.value = rTipos.data
    proveedores.value = rProv.data
  } catch {
    error.value = 'Error al cargar tipos de gasto o proveedores.'
  }
})
</script>

<template>
  <div class="formulario-masivo">

    <!-- ── Mensaje de error global ── -->
    <div v-if="error" class="alerta-error">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="alerta-error__icono">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126ZM12 15.75h.007v.008H12v-.008Z" />
      </svg>
      {{ error }}
    </div>

    <!-- ── Título sección de gastos ── -->
    <div class="seccion-titulo">
      <h3 class="seccion-titulo__texto">Gastos del Viaje</h3>
      <p class="seccion-titulo__subtexto">Agrega todos los gastos asociados a este viaje y regístralos en una sola operación.</p>
    </div>

    <!-- ── Tabla de gastos ── -->
    <div class="tabla-gastos-wrapper">
      <table class="tabla-gastos">
        <thead class="tabla-gastos__head">
          <tr>
            <th class="col-num">#</th>
            <th class="col-tipo">Tipo de gasto <span class="requerido">*</span></th>
            <th class="col-valor">Valor (COP) <span class="requerido">*</span></th>
            <th class="col-proveedor">Proveedor</th>
            <th class="col-obs">Observaciones</th>
            <th class="col-accion"></th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="(fila, index) in filas"
            :key="fila._id"
            class="tabla-gastos__fila"
            :class="{ 'tabla-gastos__fila--error': fila.errorTipo || fila.errorValor }"
          >
            <!-- # -->
            <td class="col-num td-num">{{ index + 1 }}</td>

            <!-- Tipo de gasto -->
            <td class="col-tipo">
              <select
                v-model="fila.tipo_gasto_id"
                class="input-tabla"
                :class="{ 'input-tabla--error': fila.errorTipo }"
                @change="fila.errorTipo = false"
              >
                <option value="" disabled>Seleccionar tipo...</option>
                <option v-for="t in tiposGasto" :key="t.id" :value="t.id">{{ t.nombre }}</option>
              </select>
            </td>

            <!-- Valor -->
            <td class="col-valor">
              <input
                v-model.number="fila.valor"
                type="number"
                min="1"
                placeholder="0"
                class="input-tabla input-tabla--right"
                :class="{ 'input-tabla--error': fila.errorValor }"
                @input="fila.errorValor = false"
              />
            </td>

            <!-- Proveedor -->
            <td class="col-proveedor">
              <div class="proveedor-cell">
                <select
                  v-model="fila.usarProveedorRegistrado"
                  class="input-tabla input-tabla--proveedor-tipo"
                >
                  <option :value="false">Manual</option>
                  <option :value="true">Registrado</option>
                </select>
                <input
                  v-if="!fila.usarProveedorRegistrado"
                  v-model="fila.proveedor_manual"
                  type="text"
                  placeholder="Nombre del proveedor"
                  class="input-tabla input-tabla--proveedor-nombre"
                />
                <select
                  v-else
                  v-model="fila.proveedor_id"
                  class="input-tabla input-tabla--proveedor-nombre"
                >
                  <option :value="null">Sin proveedor</option>
                  <option v-for="p in proveedores" :key="p.id" :value="p.id">{{ p.nombre }}</option>
                </select>
              </div>
            </td>

            <!-- Observaciones -->
            <td class="col-obs">
              <input
                v-model="fila.observaciones"
                type="text"
                placeholder="Detalles adicionales..."
                class="input-tabla"
              />
            </td>

            <!-- Acción: eliminar -->
            <td class="col-accion td-accion">
              <button
                type="button"
                class="btn-eliminar"
                :disabled="filas.length === 1"
                :title="filas.length === 1 ? 'Debe haber al menos un gasto' : 'Eliminar fila'"
                @click="eliminarFila(index)"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                </svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- ── Botón Agregar Fila ── -->
      <button type="button" class="btn-agregar" @click="agregarFila">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Agregar otro gasto
      </button>

      <!-- ── Info Alert ── -->
      <div class="info-alert">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a.75.75 0 000 1.5h.253a.25.25 0 01.244.304l-.459 2.066A1.75 1.75 0 0010.747 15H11a.75.75 0 000-1.5h-.253a.25.25 0 01-.244-.304l.459-2.066A1.75 1.75 0 009.253 9H9z" clip-rule="evenodd" />
        </svg>
        El número de manifiesto y la fecha se asignarán automáticamente a cada gasto.
      </div>

      <!-- ── Resumen total ── -->
      <div class="resumen">
        <div class="resumen__item">
          <p class="resumen__label">Cantidad de gastos</p>
          <p class="resumen__valor resumen__valor--cantidad">{{ cantidadGastos }}</p>
        </div>
        <div class="resumen__item resumen__item--right">
          <p class="resumen__label">Total de gastos (COP)</p>
          <p class="resumen__valor resumen__valor--monto">{{ formatMoneda(totalGastos) }}</p>
        </div>
      </div>

      <!-- ── Botones ── -->
      <div class="acciones">
        <button
          type="button"
          class="btn-cancelar"
          @click="$emit('cancelado')"
          :disabled="cargando"
        >
          Cancelar
        </button>
        <button
          type="button"
          class="btn-registrar"
          :disabled="cargando"
          @click="handleSubmit"
        >
          <svg v-if="cargando" class="btn-registrar__spinner" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          {{ cargando ? 'Guardando...' : textoBoton }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.formulario-masivo {
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: inherit;
}

/* ── Título de sección ── */
.seccion-titulo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.seccion-titulo__texto {
  font-size: 1rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
}

.seccion-titulo__subtexto {
  font-size: 0.8rem;
  color: #6b7280;
  margin: 0;
}

.btn-agregar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 10px;
  width: 100%;
  background: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #3b82f6;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-agregar:hover { background: #f1f5f9; border-color: #94a3b8; color: #2563eb; }
.btn-agregar svg { width: 16px; height: 16px; }

/* ── Info Alert ── */
.info-alert {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #1e40af;
}

.info-alert svg {
  width: 18px;
  height: 18px;
  color: #3b82f6;
  flex-shrink: 0;
}

/* ── Tabla de gastos ── */
.tabla-gastos-wrapper {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.tabla-gastos {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.8rem;
}

.tabla-gastos__head { background: #1e293b; }

.tabla-gastos__head th {
  padding: 9px 10px;
  text-align: left;
  font-size: 0.7rem;
  font-weight: 600;
  color: #cbd5e1;
  letter-spacing: 0.03em;
  white-space: nowrap;
}

.requerido { color: #f87171; }

.tabla-gastos__fila {
  border-bottom: 1px solid #f1f5f9;
  transition: background 0.1s;
}

.tabla-gastos__fila:last-child { border-bottom: none; }
.tabla-gastos__fila:hover { background: #f8fafc; }
.tabla-gastos__fila--error { background: #fff7f7; }

.tabla-gastos__fila td {
  padding: 7px 8px;
  vertical-align: top;
}

.col-num      { width: 36px; }
.col-tipo     { width: 160px; min-width: 140px; }
.col-valor    { width: 110px; min-width: 90px; }
.col-proveedor { width: 220px; min-width: 180px; }
.col-obs      { min-width: 160px; }
.col-accion   { width: 40px; }

.td-num {
  text-align: center;
  font-weight: 700;
  color: #6b7280;
  font-size: 0.75rem;
}

.td-accion { text-align: center; }

/* ── Inputs de tabla ── */
.input-tabla {
  width: 100%;
  padding: 5px 7px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 0.78rem;
  color: #1f2937;
  background: #fff;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
}

.input-tabla:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.12);
}

.input-tabla--error {
  border-color: #f87171 !important;
  background: #fff7f7;
}

.input-tabla--right { text-align: right; }

.proveedor-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.input-tabla--proveedor-tipo {
  font-size: 0.7rem;
  padding: 3px 5px;
  color: #6b7280;
  border-color: #e2e8f0;
}

/* ── Botón eliminar fila ── */
.btn-eliminar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #ef4444;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-eliminar:hover:not(:disabled) { background: #fee2e2; }
.btn-eliminar:disabled { opacity: 0.25; cursor: not-allowed; }
.btn-eliminar svg { width: 15px; height: 15px; }

/* ── Resumen ── */
.resumen {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px 24px;
}

.resumen__item { display: flex; flex-direction: column; }
.resumen__item--right { text-align: right; align-items: flex-end; }

.resumen__label {
  font-size: 0.8rem;
  font-weight: 600;
  color: #475569;
  margin: 0 0 4px 0;
}

.resumen__valor { font-size: 1.5rem; font-weight: 800; margin: 0; }
.resumen__valor--cantidad { color: #3b82f6; }
.resumen__valor--monto { color: #2563eb; }

/* ── Botones de acción ── */
.acciones {
  display: flex;
  gap: 12px;
  justify-content: space-between;
  padding-top: 12px;
}

.btn-cancelar {
  flex: 1;
  max-width: 30%;
  padding: 12px;
  background: #f1f5f9;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-cancelar:hover:not(:disabled) { background: #e2e8f0; }
.btn-cancelar:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-registrar {
  flex: 2;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #2563eb;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  color: #fff;
  cursor: pointer;
  transition: background 0.15s, box-shadow 0.15s;
}

.btn-registrar:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: 0 4px 10px rgba(37, 99, 235, 0.35);
}

.btn-registrar:disabled { opacity: 0.6; cursor: not-allowed; box-shadow: none; }

.btn-registrar__spinner {
  width: 14px;
  height: 14px;
  animation: spin 0.7s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
</style>
