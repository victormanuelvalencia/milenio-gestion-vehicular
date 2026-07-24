import { defineStore } from 'pinia'
import api from '@/services/api'
import router from '@/router'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(correo, contrasena) {
      try {
        const response = await api.post('/login', { correo, contrasena })
        this.token = response.data.token_acceso
        localStorage.setItem('token', this.token)
        router.push('/')
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.detail || 'Error al iniciar sesión'
        return { success: false, message }
      }
    },
    logout() {
      this.token = null
      localStorage.removeItem('token')
      router.push('/login')
    },
  },
})
