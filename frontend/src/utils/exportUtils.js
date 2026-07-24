import * as xlsx from 'xlsx'
import { jsPDF } from 'jspdf'
import autoTable from 'jspdf-autotable'

export const exportarAExcel = (datos, columnas, nombreArchivo) => {
  if (!datos || datos.length === 0) {
    alert('No hay datos para exportar.')
    return
  }

  // Mapear los datos según las columnas
  const datosMapeados = datos.map(fila => {
    const filaExport = {}
    columnas.forEach(col => {
      filaExport[col.header] = typeof col.key === 'function' ? col.key(fila) : fila[col.key]
    })
    return filaExport
  })

  const hoja = xlsx.utils.json_to_sheet(datosMapeados)
  const libro = xlsx.utils.book_new()
  xlsx.utils.book_append_sheet(libro, hoja, 'Reporte')
  xlsx.writeFile(libro, `${nombreArchivo}.xlsx`)
}

export const exportarAPDF = (datos, columnas, nombreArchivo, titulo) => {
  if (!datos || datos.length === 0) {
    alert('No hay datos para exportar.')
    return
  }

  const doc = new jsPDF()

  doc.setFontSize(18)
  doc.text(titulo, 14, 22)
  doc.setFontSize(11)
  doc.setTextColor(100)
  doc.text(`Generado el: ${new Date().toLocaleDateString('es-CO')}`, 14, 30)

  const head = [columnas.map(c => c.header)]
  const body = datos.map(fila => {
    return columnas.map(col => {
      return typeof col.key === 'function' ? col.key(fila) : fila[col.key]
    })
  })

  autoTable(doc, {
    startY: 35,
    head: head,
    body: body,
    theme: 'grid',
    styles: { fontSize: 9, cellPadding: 3 },
    headStyles: { fillColor: [30, 41, 59], textColor: 255 }, // bg-slate-800
  })

  doc.save(`${nombreArchivo}.pdf`)
}
