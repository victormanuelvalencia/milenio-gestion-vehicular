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

export const conductoresService = {
  obtenerTodos: () => api.get('/conductores'),
  obtenerPorId: (id) => api.get(`/conductores/${id}`),
  crear: (datos) => api.post('/conductores', datos),
  actualizar: (id, datos) => api.put(`/conductores/${id}`, datos),
  eliminar: (id) => api.delete(`/conductores/${id}`),
}

export const viajesService = {
  obtenerTodos: () => api.get('/viajes'),
  obtenerPorId: (id) => api.get(`/viajes/${id}`),
  obtenerGastos: (id) => api.get(`/viajes/${id}/gastos`),
  crear: (datos) => api.post('/viajes', datos),
  actualizar: (id, datos) => api.put(`/viajes/${id}`, datos),
  eliminar: (id) => api.delete(`/viajes/${id}`),
}

export const mantenimientosService = {
  obtenerTodos: () => api.get('/mantenimientos'),
  obtenerPorId: (id) => api.get(`/mantenimientos/${id}`),
  crear: (datos) => api.post('/mantenimientos', datos),
  actualizar: (id, datos) => api.put(`/mantenimientos/${id}`, datos),
  eliminar: (id) => api.delete(`/mantenimientos/${id}`),
}

export const mantenimientosProgramadosService = {
  obtenerTodos: () => api.get('/mantenimientos-programados'),
  obtenerPorId: (id) => api.get(`/mantenimientos-programados/${id}`),
  crear: (datos) => api.post('/mantenimientos-programados', datos),
  actualizar: (id, datos) => api.put(`/mantenimientos-programados/${id}`, datos),
  eliminar: (id) => api.delete(`/mantenimientos-programados/${id}`),
}

export const reportesService = {
  gastosPorVehiculo: (params) => api.get('/reportes/gastos-por-vehiculo', { params }),
  gastosPorMes: (params) => api.get('/reportes/gastos-por-mes', { params }),
  utilidadPorPeriodo: (params) => api.get('/reportes/utilidad-por-periodo', { params }),
  historialVehiculo: (params) => api.get('/reportes/historial-vehiculo', { params }),
  costosEntreFechas: (params) => api.get('/reportes/costos-entre-fechas', { params }),
  gastosPorProveedor: (params) => api.get('/reportes/gastos-por-proveedor', { params }),
}

export const usuariosService = {
  obtenerTodos: () => api.get('/usuarios'),
  obtenerPorId: (id) => api.get(`/usuarios/${id}`),
  crear: (datos) => api.post('/usuarios', datos),
  actualizar: (id, datos) => api.put(`/usuarios/${id}`, datos),
  eliminar: (id) => api.delete(`/usuarios/${id}`),
  cambiarEstado: (id, activo) => api.patch(`/usuarios/${id}/estado`, { activo }),
  cambiarRol: (id, rol) => api.patch(`/usuarios/${id}/rol`, { rol }),
  cambiarContrasena: (id, datos) => api.patch(`/usuarios/${id}/contrasena`, datos),
}
