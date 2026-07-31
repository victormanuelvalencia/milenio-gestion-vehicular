<script setup>
import { ref, onMounted , watch } from 'vue'
import { useRoute } from 'vue-router'
import { gastosService } from '@/services/modules'
import FormularioGasto from '@/components/gastos/FormularioGasto.vue'

const route = useRoute()
const gasto = ref(null)
const cargando = ref(true)
const error = ref('')


watch(error, (val) => { if (val) setTimeout(() => error.value = '', 3000) })

onMounted(async () => {
  try {
    const res = await gastosService.obtenerPorId(route.params.id)
    gasto.value = res.data
  } catch {
    error.value = 'No se pudo cargar el gasto.'
  } finally {
    cargando.value = false
  }
})
</script>

<template>
  <div>
    <div v-if="cargando" class="text-center py-16 text-gray-400">Cargando...</div>
    <div v-else-if="error" class="p-4 bg-red-50 text-red-600 rounded-lg">{{ error }}</div>
    <FormularioGasto v-else modo="detalle" :gasto-inicial="gasto" />
  </div>
</template>
