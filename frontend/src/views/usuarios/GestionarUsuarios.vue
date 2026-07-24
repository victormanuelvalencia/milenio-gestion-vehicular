<script setup>
import { ref, computed, onMounted } from 'vue'
import { usuariosService } from '@/services/modules'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const usuarios = ref([])
const cargando = ref(false)
const error = ref('')
const mensajeExito = ref('')

// Modales
const modalCrearAbierto = ref(false)
const modalEditarAbierto = ref(false)
const modalEliminarAbierto = ref(false)
const usuarioSeleccionado = ref(null)

// Formularios
const formularioCrear = ref({
  nombre: '',
  correo: '',
  contrasena: '',
  confirmar_contrasena: '',
  rol: 'USUARIO',
  activo: true
})

const formularioEditar = ref({
  nombre: '',
  correo: '',
  rol: 'USUARIO',
  activo: true
})

const cargandoAccion = ref(false)

const cargarUsuarios = async () => {
  cargando.value = true
  error.value = ''
  try {
    const res = await usuariosService.obtenerTodos()
    usuarios.value = res.data
  } catch {
    error.value = 'Error al cargar los usuarios.'
  } finally {
    cargando.value = false
  }
}

const abrirModalCrear = () => {
  formularioCrear.value = {
    nombre: '',
    correo: '',
    contrasena: '',
    confirmar_contrasena: '',
    rol: 'USUARIO',
    activo: true
  }
  modalCrearAbierto.value = true
}

const crearUsuario = async () => {
  if (formularioCrear.value.contrasena !== formularioCrear.value.confirmar_contrasena) {
    alert("Las contraseñas no coinciden")
    return
  }
  cargandoAccion.value = true
  try {
    await usuariosService.crear(formularioCrear.value)
    mensajeExito.value = 'Usuario creado correctamente.'
    modalCrearAbierto.value = false
    await cargarUsuarios()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al crear el usuario.')
  } finally {
    cargandoAccion.value = false
  }
}

const abrirModalEditar = (usuario) => {
  usuarioSeleccionado.value = usuario
  formularioEditar.value = {
    nombre: usuario.nombre,
    correo: usuario.correo,
    rol: usuario.rol,
    activo: usuario.activo
  }
  modalEditarAbierto.value = true
}

const editarUsuario = async () => {
  cargandoAccion.value = true
  try {
    await usuariosService.actualizar(usuarioSeleccionado.value.id, formularioEditar.value)
    mensajeExito.value = 'Usuario actualizado correctamente.'
    modalEditarAbierto.value = false
    await cargarUsuarios()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al actualizar el usuario.')
  } finally {
    cargandoAccion.value = false
  }
}

const toggleEstado = async (usuario) => {
  try {
    await usuariosService.cambiarEstado(usuario.id, !usuario.activo)
    await cargarUsuarios()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al cambiar estado.')
  }
}

const abrirModalEliminar = (usuario) => {
  usuarioSeleccionado.value = usuario
  modalEliminarAbierto.value = true
}

const eliminarUsuario = async () => {
  cargandoAccion.value = true
  try {
    await usuariosService.eliminar(usuarioSeleccionado.value.id)
    mensajeExito.value = 'Usuario eliminado correctamente.'
    modalEliminarAbierto.value = false
    await cargarUsuarios()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error al eliminar el usuario.')
  } finally {
    cargandoAccion.value = false
  }
}

const POR_PAGINA = 15
const paginaActual = ref(1)
const totalPaginas = computed(() => Math.ceil(usuarios.value.length / POR_PAGINA))
const usuariosPaginados = computed(() => {
  const inicio = (paginaActual.value - 1) * POR_PAGINA
  return usuarios.value.slice(inicio, inicio + POR_PAGINA)
})
const irPagina = (n) => { if (n >= 1 && n <= totalPaginas.value) paginaActual.value = n }

onMounted(cargarUsuarios)

const getBadgeColor = (rol) => {
  switch (rol) {
    case 'SUPERADMIN': return 'bg-purple-100 text-purple-800 border-purple-200'
    case 'ADMIN': return 'bg-blue-100 text-blue-800 border-blue-200'
    default: return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return '—'
  const date = new Date(fechaStr)
  return new Intl.DateTimeFormat('es-CO', { year: 'numeric', month: 'short', day: '2-digit' }).format(date)
}
</script>

<template>
  <div>
    <div class="mb-6 flex justify-between items-center">
      <h2 class="text-2xl font-bold text-gray-800">Administración de Usuarios</h2>
      <button 
        @click="abrirModalCrear" 
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm flex items-center gap-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
        </svg>
        Nuevo usuario
      </button>
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
            <th class="px-4 py-3 w-[25%] text-left">Nombre / Correo</th>
            <th class="px-4 py-3 w-[15%]">Rol</th>
            <th class="px-4 py-3 w-[15%]">Estado</th>
            <th class="px-4 py-3 w-[20%]">Fecha creación</th>
            <th class="px-4 py-3 w-[25%]">Acciones</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-if="usuarios.length === 0">
            <td colspan="5" class="text-center py-10 text-gray-400">No hay usuarios registrados.</td>
          </tr>
          <tr v-for="u in usuariosPaginados" :key="u.id" class="hover:bg-slate-50 transition-colors">
            <td class="px-4 py-3 text-left">
              <div class="font-medium text-gray-800">{{ u.nombre }}</div>
              <div class="text-xs text-gray-500">{{ u.correo }}</div>
            </td>
            <td class="px-4 py-3">
              <span :class="['px-2.5 py-1 rounded-full text-xs font-semibold border', getBadgeColor(u.rol)]">
                {{ u.rol }}
              </span>
            </td>
            <td class="px-4 py-3">
              <button 
                @click="toggleEstado(u)"
                class="px-2 py-1 rounded text-xs font-medium border transition-colors focus:outline-none"
                :class="u.activo ? 'bg-green-50 text-green-700 border-green-200 hover:bg-green-100' : 'bg-red-50 text-red-700 border-red-200 hover:bg-red-100'"
              >
                {{ u.activo ? 'Activo' : 'Inactivo' }}
              </button>
            </td>
            <td class="px-4 py-3 text-gray-500 text-xs">
              {{ formatearFecha(u.fecha_creacion) }}
            </td>
            <td class="px-4 py-3">
              <div class="flex justify-center gap-3">
                <button @click="abrirModalEditar(u)" title="Editar" class="text-blue-500 hover:text-blue-700 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10" /></svg>
                </button>
                <button @click="abrirModalEliminar(u)" title="Eliminar" class="text-red-500 hover:text-red-700 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5"><path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" /></svg>
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
      <span class="ml-2 text-sm text-gray-500">Página {{ paginaActual }} de {{ totalPaginas }} · {{ usuarios.length }} registros</span>
    </div>

    <!-- Modal Crear -->
    <div v-if="modalCrearAbierto" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Crear Nuevo Usuario</h3>
          <button @click="modalCrearAbierto = false" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="crearUsuario" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre completo *</label>
            <input v-model="formularioCrear.nombre" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" placeholder="Ej: Juan Pérez" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Correo electrónico *</label>
            <input v-model="formularioCrear.correo" type="email" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" placeholder="ejemplo@mileniotransportadora.com" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Contraseña *</label>
              <input v-model="formularioCrear.contrasena" type="password" required minlength="6" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Confirmar *</label>
              <input v-model="formularioCrear.confirmar_contrasena" type="password" required minlength="6" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" />
            </div>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
              <select v-model="formularioCrear.rol" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                <option value="USUARIO">USUARIO</option>
                <option value="ADMIN">ADMIN</option>
                <option value="SUPERADMIN">SUPERADMIN</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="formularioCrear.activo" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="modalCrearAbierto = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="cargandoAccion" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ cargandoAccion ? 'Guardando...' : 'Crear Usuario' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Editar -->
    <div v-if="modalEditarAbierto" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-lg font-bold text-gray-800">Editar Usuario</h3>
          <button @click="modalEditarAbierto = false" class="text-gray-400 hover:text-gray-600">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <form @submit.prevent="editarUsuario" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nombre completo *</label>
            <input v-model="formularioEditar.nombre" type="text" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Correo electrónico *</label>
            <input v-model="formularioEditar.correo" type="email" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Rol</label>
              <select v-model="formularioEditar.rol" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                <option value="USUARIO">USUARIO</option>
                <option value="ADMIN">ADMIN</option>
                <option value="SUPERADMIN">SUPERADMIN</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select v-model="formularioEditar.activo" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm">
                <option :value="true">Activo</option>
                <option :value="false">Inactivo</option>
              </select>
            </div>
          </div>
          <div class="pt-4 flex justify-end gap-3 border-t border-gray-100 mt-6">
            <button type="button" @click="modalEditarAbierto = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button type="submit" :disabled="cargandoAccion" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg hover:bg-blue-700 disabled:opacity-50">
              {{ cargandoAccion ? 'Guardando...' : 'Guardar Cambios' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Eliminar -->
    <div v-if="modalEliminarAbierto" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm overflow-hidden">
        <div class="p-6 text-center">
          <div class="w-16 h-16 rounded-full bg-red-100 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          </div>
          <h3 class="text-lg font-bold text-gray-800 mb-2">¿Eliminar usuario?</h3>
          <p class="text-sm text-gray-500 mb-6">
            Esta acción no se puede deshacer. ¿Estás seguro que deseas eliminar a <strong>{{ usuarioSeleccionado?.nombre }}</strong>?
          </p>
          <div class="flex justify-center gap-3">
            <button @click="modalEliminarAbierto = false" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">Cancelar</button>
            <button @click="eliminarUsuario" :disabled="cargandoAccion" class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-lg hover:bg-red-700 disabled:opacity-50">
              {{ cargandoAccion ? 'Eliminando...' : 'Sí, eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
