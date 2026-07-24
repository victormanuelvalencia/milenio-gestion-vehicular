<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const reportes = [
  { 
    id: 'gastos-vehiculo', 
    titulo: 'Gastos por Vehículo', 
    descripcion: 'Consulta los gastos asociados a un vehículo específico en un rango de fechas.',
    ruta: '/reportes/gastos-por-vehiculo',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 0 1-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 0 0-3.213-9.193 2.056 2.056 0 0 0-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 0 0-10.026 0 1.106 1.106 0 0 0-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12" /></svg>' 
  },
  { 
    id: 'gastos-mes', 
    titulo: 'Gastos por Mes', 
    descripcion: 'Visualiza el consolidado de gastos organizados mensualmente por año.',
    ruta: '/reportes/gastos-por-mes',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" /></svg>' 
  },
  { 
    id: 'gastos-tipo', 
    titulo: 'Gastos por Tipo', 
    descripcion: 'Analiza en qué tipos de gasto se invierte más dinero en un rango de fechas.',
    ruta: '/reportes/gastos-por-tipo',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" /><path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" /></svg>' 
  },
  { 
    id: 'historial-vehiculo', 
    titulo: 'Historial de un Vehículo', 
    descripcion: 'Revisa todos los gastos históricos registrados para un vehículo.',
    ruta: '/reportes/historial-vehiculo',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" /></svg>' 
  },
  { 
    id: 'costos-fechas', 
    titulo: 'Costos entre Fechas', 
    descripcion: 'Genera un reporte de todos los gastos comprendidos entre dos fechas.',
    ruta: '/reportes/costos-fechas',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0 1 15.797 2.101c.727.198 1.453-.342 1.453-1.096V4.22c0-.756-.728-1.293-1.453-1.096a59.769 59.769 0 0 1-15.797 2.101c-.727.198-1.453.342-1.453 1.096v11.334c0 .756.728 1.294 1.453 1.096ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 6a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Zm0 13.5a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" /></svg>' 
  },
  { 
    id: 'gastos-proveedor', 
    titulo: 'Gastos por Proveedor', 
    descripcion: 'Consulta todos los gastos realizados a nombre de un proveedor específico.',
    ruta: '/reportes/gastos-proveedor',
    icono: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-7 h-7"><path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" /></svg>' 
  }
]

const irAReporte = (ruta) => {
  router.push(ruta)
}
</script>

<template>
  <div class="max-w-5xl mx-auto py-8 px-4">
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-slate-800">Módulo de Reportes</h1>
      <p class="text-slate-500 mt-2">Selecciona el reporte que deseas generar para analizar la información.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="rep in reportes" 
        :key="rep.id"
        @click="irAReporte(rep.ruta)"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 cursor-pointer hover:-translate-y-1 hover:shadow-md transition-all duration-300 group flex flex-col items-center text-center"
      >
        <div 
          class="w-16 h-16 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors duration-300"
          v-html="rep.icono"
        ></div>
        <h3 class="text-lg font-bold text-slate-800 mb-2">{{ rep.titulo }}</h3>
        <p class="text-sm text-slate-500 line-clamp-3">{{ rep.descripcion }}</p>
      </div>
    </div>
  </div>
</template>
