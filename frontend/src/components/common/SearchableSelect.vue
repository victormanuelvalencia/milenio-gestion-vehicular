<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

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
const inputRef = ref(null)

// La opción seleccionada actualmente
const selectedOption = computed(() =>
  props.options.find(opt => opt.value === props.modelValue) ?? null
)

// Opciones filtradas por lo que escribe el usuario
const filteredOptions = computed(() => {
  const q = searchQuery.value.toLowerCase().trim()
  if (!q) return props.options
  return props.options.filter(opt => opt.label.toLowerCase().includes(q))
})

// Lo que se muestra en el input:
// - si está abierto: lo que escribe el usuario (para filtrar)
// - si está cerrado: el label de la opción seleccionada (o vacío)
const inputValue = computed({
  get() {
    if (isOpen.value) return searchQuery.value
    return selectedOption.value ? selectedOption.value.label : ''
  },
  set(val) {
    searchQuery.value = val
  }
})

function openDropdown() {
  if (props.disabled) return
  isOpen.value = true
  searchQuery.value = ''
  nextTick(() => inputRef.value?.focus())
}

function onInputChange(e) {
  searchQuery.value = e.target.value
}

function selectOption(option) {
  emit('update:modelValue', option.value)
  emit('change', option.value)
  isOpen.value = false
  searchQuery.value = ''
}

function clearSelection(e) {
  e.stopPropagation()
  emit('update:modelValue', null)
  emit('change', null)
  searchQuery.value = ''
  isOpen.value = false
}

function handleClickOutside(e) {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false
    searchQuery.value = ''
  }
}

onMounted(() => document.addEventListener('mousedown', handleClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', handleClickOutside))
</script>

<template>
  <div class="relative w-full" ref="containerRef">

    <!-- Input oculto para validación nativa (required) -->
    <input
      v-if="required"
      type="text"
      :value="modelValue ?? ''"
      class="absolute opacity-0 w-0 h-0 pointer-events-none"
      :required="required"
      tabindex="-1"
      aria-hidden="true"
    />

    <!-- Campo principal: es el buscador y el display en uno solo -->
    <div class="relative">
      <input
        ref="inputRef"
        type="text"
        :value="inputValue"
        :placeholder="isOpen ? 'Escribe para filtrar...' : placeholder"
        :disabled="disabled"
        autocomplete="off"
        class="w-full px-3 py-2 pr-9 border rounded-lg text-sm bg-white transition-all focus:outline-none"
        :class="[
          disabled
            ? 'border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed'
            : 'border-gray-300 cursor-pointer hover:border-blue-400',
          isOpen
            ? 'ring-2 ring-blue-500 border-blue-500'
            : '',
          !selectedOption && !isOpen
            ? 'text-gray-400'
            : 'text-gray-900'
        ]"
        @click="openDropdown"
        @focus="openDropdown"
        @input="onInputChange"
      />

      <!-- Íconos a la derecha -->
      <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1 pointer-events-none">
        <!-- Botón limpiar (con pointer-events propios) -->
        <button
          v-if="selectedOption && !disabled"
          type="button"
          class="pointer-events-auto text-gray-300 hover:text-gray-600 transition-colors p-0.5 rounded"
          @mousedown.prevent="clearSelection"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <!-- Flecha -->
        <svg
          class="w-4 h-4 text-gray-400 shrink-0 transition-transform duration-200"
          :class="isOpen ? 'rotate-180' : ''"
          fill="none" viewBox="0 0 24 24" stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>

    <!-- Dropdown de opciones -->
    <div
      v-if="isOpen"
      class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-lg overflow-hidden"
    >
      <div class="max-h-56 overflow-y-auto py-1">
        <div
          v-if="filteredOptions.length === 0"
          class="px-4 py-3 text-sm text-gray-400 text-center italic"
        >
          Sin coincidencias
        </div>
        <div
          v-for="opt in filteredOptions"
          :key="opt.value"
          @mousedown.prevent="selectOption(opt)"
          class="px-4 py-2 text-sm cursor-pointer transition-colors flex items-center gap-2"
          :class="opt.value === modelValue
            ? 'bg-blue-50 text-blue-700 font-medium'
            : 'text-gray-700 hover:bg-gray-50'"
        >
          <svg
            v-if="opt.value === modelValue"
            class="w-3.5 h-3.5 text-blue-600 shrink-0"
            fill="none" viewBox="0 0 24 24" stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          <span :class="opt.value !== modelValue ? 'ml-5' : ''">{{ opt.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
