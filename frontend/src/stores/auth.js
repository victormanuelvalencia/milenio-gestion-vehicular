import { defineStore } from 'pinia'
import api from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    usuario: localStorage.getItem('usuario') ? JSON.parse(localStorage.getItem('usuario')) : null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRol: (state) => state.usuario?.rol || 'USUARIO',
    userNombre: (state) => state.usuario?.nombre || 'Usuario',
  },
  actions: {
    async login(correo, contrasena) {
      try {
        const response = await api.post('/login', { correo, contrasena })
        this.token = response.data.token_acceso
        localStorage.setItem('token', this.token)
        
        // Parse JWT to extract user info
        try {
          const payloadBase64 = this.token.split('.')[1]
          const decodedJson = atob(payloadBase64)
          const payload = JSON.parse(decodedJson)
          this.usuario = {
            nombre: payload.nombre || 'Usuario',
            rol: payload.rol || 'USUARIO'
          }
          localStorage.setItem('usuario', JSON.stringify(this.usuario))
        } catch (e) {
          console.error('Error parsing token:', e)
        }

        router.push('/')
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.detail || 'Error al iniciar sesión'
        return { success: false, message }
      }
    },
    logout() {
      this.token = null
      this.usuario = null
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
      router.push('/login')
    },
  },
})
