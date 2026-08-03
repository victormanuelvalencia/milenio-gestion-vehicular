/**
 * Composable centralizado para control de permisos por roles.
 *
 * Roles disponibles:
 *   - SUPERADMIN: acceso completo (crear, editar, eliminar, consultar).
 *   - ADMIN / USUARIO: solo lectura (consultar y reportes).
 *
 */
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function usePermisos() {
  const authStore = useAuthStore()

  /** true si el usuario tiene rol SUPERADMIN */
  const esSuperAdmin = computed(() => authStore.userRol === 'SUPERADMIN')

  /**
   * true si el usuario puede realizar operaciones de escritura
   * (crear, editar, eliminar).
   * Actualmente equivale a esSuperAdmin; diseñado para ser extensible.
   */
  const puedeEscribir = esSuperAdmin

  return {
    esSuperAdmin,
    puedeEscribir,
  }
}
