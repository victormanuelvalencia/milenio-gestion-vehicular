import api from './api'

export const vehiculosService = {
  obtenerTodos: () => api.get('/vehiculos'),
  obtenerPorId: (id) => api.get(`/vehiculos/${id}`),
  crear: (datos) => api.post('/vehiculos', datos),
  actualizar: (id, datos) => api.put(`/vehiculos/${id}`, datos),
  eliminar: (id) => api.delete(`/vehiculos/${id}`),
  cambiarEstado: (id, estadoActual) =>
    api.put(`/vehiculos/${id}`, { estado: !estadoActual }),
}

export const tiposGastoService = {
  obtenerTodos: () => api.get('/tipos-gasto'),
  obtenerPorId: (id) => api.get(`/tipos-gasto/${id}`),
  crear: (datos) => api.post('/tipos-gasto', datos),
  actualizar: (id, datos) => api.put(`/tipos-gasto/${id}`, datos),
  eliminar: (id) => api.delete(`/tipos-gasto/${id}`),
}

export const proveedoresService = {
  obtenerTodos: () => api.get('/proveedores'),
  obtenerPorId: (id) => api.get(`/proveedores/${id}`),
  crear: (datos) => api.post('/proveedores', datos),
  actualizar: (id, datos) => api.put(`/proveedores/${id}`, datos),
  eliminar: (id) => api.delete(`/proveedores/${id}`),
}

export const gastosService = {
  obtenerTodos: () => api.get('/gastos'),
  obtenerPorId: (id) => api.get(`/gastos/${id}`),
  crear: (datos) => api.post('/gastos', datos),
  actualizar: (id, datos) => api.put(`/gastos/${id}`, datos),
  eliminar: (id) => api.delete(`/gastos/${id}`),
}

export const reportesService = {
  gastosPorVehiculo: (params) => api.get('/reportes/gastos-por-vehiculo', { params }),
  gastosPorMes: (params) => api.get('/reportes/gastos-por-mes', { params }),
  gastosPorTipo: (params) => api.get('/reportes/gastos-por-tipo', { params }),
  historialVehiculo: (params) => api.get('/reportes/historial-vehiculo', { params }),
  costosEntreFechas: (params) => api.get('/reportes/costos-entre-fechas', { params }),
  gastosPorProveedor: (params) => api.get('/reportes/gastos-por-proveedor', { params }),
}
