<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number, null],
    default: null
  },
  options: {
    type: Array, // Array of { value: any, label: string }
    required: true
  },
  placeholder: {
    type: String,
    default: 'Seleccione...'
  },
  disabled: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOpen = ref(false)
const searchQuery = ref('')
const containerRef = ref(null)
const searchInputRef = ref(null)

const selectedOption = computed(() => 
  props.options.find(opt => opt.value === props.modelValue)
)

const filteredOptions = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return props.options
  return props.options.filter(opt => 
    opt.label.toLowerCase().includes(q)
  )
})

const toggleOpen = () => {
  if (props.disabled) return
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    searchQuery.value = ''
    nextTick(() => {
      if (searchInputRef.value) searchInputRef.value.focus()
    })
  }
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  emit('change', option.value)
  isOpen.value = false
  searchQuery.value = ''
}

const handleClickOutside = (e) => {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<template>
  <div class="relative w-full" ref="containerRef">
    <!-- Input oculto para validación HTML (required) -->
    <input 
      v-if="required"
      type="text" 
      :value="modelValue" 
      class="absolute opacity-0 w-0 h-0 pointer-events-none" 
      :required="required"
    />

    <!-- Botón del Select -->
    <div 
      @click="toggleOpen"
      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm bg-white flex justify-between items-center transition-colors min-h-[38px]"
      :class="[
        disabled ? 'bg-gray-50 text-gray-500 cursor-not-allowed' : 'cursor-pointer hover:border-blue-400',
        isOpen ? 'ring-2 ring-blue-500 border-blue-500' : ''
      ]"
    >
      <span class="truncate" :class="!selectedOption ? 'text-gray-500' : 'text-gray-900'">
        {{ selectedOption ? selectedOption.label : placeholder }}
      </span>
      <svg class="w-4 h-4 text-gray-400 shrink-0 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
      </svg>
    </div>

    <!-- Menú Desplegable -->
    <div 
      v-if="isOpen" 
      class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden flex flex-col"
    >
      <!-- Input de Búsqueda -->
      <div class="p-2 border-b border-gray-100 bg-gray-50 shrink-0">
        <input 
          ref="searchInputRef"
          type="text" 
          v-model="searchQuery" 
          placeholder="Buscar..." 
          class="w-full px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
          @click.stop
        />
      </div>

      <!-- Lista de Opciones -->
      <div class="max-h-60 overflow-y-auto py-1">
        <div 
          v-if="filteredOptions.length === 0" 
          class="px-4 py-2 text-sm text-gray-500 text-center"
        >
          No se encontraron resultados
        </div>
        <div 
          v-for="opt in filteredOptions" 
          :key="opt.value"
          @click="selectOption(opt)"
          class="px-4 py-2 text-sm cursor-pointer transition-colors"
          :class="opt.value === modelValue ? 'bg-blue-50 text-blue-700 font-medium' : 'text-gray-700 hover:bg-gray-100'"
        >
          {{ opt.label }}
        </div>
      </div>
    </div>
  </div>
</template>
