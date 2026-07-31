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
const inputQuery = ref('')
const containerRef = ref(null)
const inputRef = ref(null)
const isTyping = ref(false)

const selectedOption = computed(() =>
  props.options.find(opt => opt.value === props.modelValue) || null
)

// Texto visible en el input
const displayText = computed(() => {
  if (isTyping.value) return inputQuery.value
  return selectedOption.value ? selectedOption.value.label : ''
})

const filteredOptions = computed(() => {
  if (!isTyping.value || !inputQuery.value.trim()) return props.options
  const q = inputQuery.value.toLowerCase().trim()
  return props.options.filter(opt =>
    opt.label.toLowerCase().includes(q)
  )
})

const openDropdown = () => {
  if (props.disabled) return
  isOpen.value = true
  isTyping.value = true
  inputQuery.value = ''
  nextTick(() => inputRef.value?.focus())
}

const onInput = (e) => {
  inputQuery.value = e.target.value
  isTyping.value = true
  isOpen.value = true
}

const onFocus = () => {
  if (props.disabled) return
  isOpen.value = true
  isTyping.value = true
  inputQuery.value = ''
}

const selectOption = (option) => {
  emit('update:modelValue', option.value)
  emit('change', option.value)
  isOpen.value = false
  isTyping.value = false
  inputQuery.value = ''
}

const clearSelection = (e) => {
  e.stopPropagation()
  emit('update:modelValue', null)
  emit('change', null)
  inputQuery.value = ''
  isTyping.value = false
  isOpen.value = false
}

const handleClickOutside = (e) => {
  if (containerRef.value && !containerRef.value.contains(e.target)) {
    isOpen.value = false
    isTyping.value = false
    inputQuery.value = ''
  }
}

// Si el valor externo cambia y no estamos escribiendo, sincroniza
watch(() => props.modelValue, () => {
  if (!isTyping.value) inputQuery.value = ''
})

onMounted(() => document.addEventListener('mousedown', handleClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', handleClickOutside))
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
      tabindex="-1"
    />

    <!-- Campo principal combobox -->
    <div
      class="relative w-full"
      @click="openDropdown"
    >
      <input
        ref="inputRef"
        type="text"
        :value="displayText"
        :placeholder="placeholder"
        :disabled="disabled"
        class="w-full px-3 py-2 pr-8 border border-gray-300 rounded-lg text-sm bg-white transition-colors focus:outline-none"
        :class="[
          disabled ? 'bg-gray-50 text-gray-400 cursor-not-allowed' : 'cursor-pointer',
          isOpen ? 'ring-2 ring-blue-500 border-blue-500' : 'hover:border-blue-400',
          !selectedOption && !isTyping ? 'text-gray-400' : 'text-gray-900'
        ]"
        autocomplete="off"
        readonly
        @focus="onFocus"
        @input="onInput"
        @click.stop="openDropdown"
      />

      <!-- Ícono de flecha / limpiar -->
      <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-1">
        <!-- Botón limpiar cuando hay selección -->
        <button
          v-if="selectedOption && !disabled"
          type="button"
          @click="clearSelection"
          class="text-gray-300 hover:text-gray-500 transition-colors p-0.5 rounded"
        >
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <!-- Flecha -->
        <svg
          class="w-4 h-4 text-gray-400 shrink-0 transition-transform"
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
      class="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-xl overflow-hidden"
    >
      <!-- Buscador integrado en el dropdown -->
      <div class="p-2 border-b border-gray-100">
        <input
          type="text"
          v-model="inputQuery"
          placeholder="Escribe para filtrar..."
          class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-gray-50"
          @click.stop
          autofocus
        />
      </div>

      <!-- Lista -->
      <div class="max-h-56 overflow-y-auto py-1">
        <div
          v-if="filteredOptions.length === 0"
          class="px-4 py-3 text-sm text-gray-400 text-center"
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
          <!-- Checkmark para la opción seleccionada -->
          <svg v-if="opt.value === modelValue" class="w-3.5 h-3.5 text-blue-600 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="m4.5 12.75 6 6 9-13.5" />
          </svg>
          <span :class="opt.value !== modelValue ? 'ml-5' : ''">{{ opt.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
