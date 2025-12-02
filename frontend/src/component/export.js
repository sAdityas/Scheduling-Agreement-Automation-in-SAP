import { useState } from 'react'
import '../css/export.css'

export default function ExportReport() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState([])
  const [aggrNumber, setAggrNumber] = useState('')

  const handleBack = () => {
    if (window.history.length > 1) {
      window.history.back()
    } else {
      window.location.href = '/WithGrn'
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResults([])

    try {
      const fd = new FormData()
      fd.append('aggrNumber', aggrNumber)

      const res = await fetch('http://127.0.0.1:5050/getExcel', {
        method: 'POST',
        body: fd
      })

      const data = await res.json().catch(() => ({}))
      if (!res.ok) {
        setError(data?.error || 'An error occurred while processing.')
        return
      }

      const list = Array.isArray(data?.results)
        ? data.results
        : (data?.results ? [data.results] : [])

      if (list.length === 0) setError('No results returned from the server.')
      setResults(list)
    } catch (err) {
      setError(`Failed to connect to backend: ${err.message}`)
      console.error('Fetch error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleExcelExport = () => {
    if (!Array.isArray(results) || results.length === 0) return

    const headers = ['Material', 'Short Text', 'Target Qty', 'Unit of Entry', 'Open Qty']
    const rows = results.map(r => ([
      (r['Material'] ?? '').toString(),
      (r['Short Text'] ?? '').toString(),
      (r['Target Qty'] ?? '').toString(),
      (r['Unit of Entry'] ?? '').toString(),
      (r['Open Qty'] ?? '').toString(),
    ]))

    const escapeCSV = (v) => {
      const s = `${v ?? ''}`
      return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s
    }

    const csv = [
      headers.map(escapeCSV).join(','),
      ...rows.map(r => r.map(escapeCSV).join(',')),
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    const ts = aggrNumber
    a.href = url
    a.download = `${ts}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className='export-container'>
        <div className='export-title'>
            <h3>Export Report</h3>
        </div>
      {(!results || results.length === 0) ? (
        <form onSubmit={handleSubmit} className='export-form'>
          <label className='export-label'>Agreement Number:</label>
          <input
            minLength={10}
            maxLength={10}
            type='text'
            className='export-input'
            placeholder='Enter Agreement Number'
            onChange={(e) => setAggrNumber(e.target.value)}
            required
          />

          <div className='export-actions'>
            <button
              className='export-btn'
              type='submit'
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Export'}
            </button>

            <button
              className='export-btn'
              type='button'
              onClick={handleBack}
            >
              Back
            </button>
          </div>
        </form>
      ) : (
        <div className='export-results'>
          <div className='export-results-header'>
            <h2 className='export-title'>Results</h2>
          </div>

          <table className='export-table'>
            <thead>
              <tr>
                <th>Material</th>
                <th>Short Text</th>
                <th>Target Qty</th>
                <th>Unit Entry</th>
                <th>Open Qty</th>
              </tr>
            </thead>
            <tbody>
              {results.map((res, idx) => (
                <tr key={idx}>
                  <td>{res['Material']?.toString().toUpperCase() ?? '-'}</td>
                  <td>{res['Short Text']?.toString().toUpperCase() ?? '-'}</td>
                  <td>{res['Target Qty']?.toString().toUpperCase() ?? '-'}</td>
                  <td>{res['Unit of Entry']?.toString().toUpperCase() ?? '-'}</td>
                  <td>{res['Open Qty']?.toString().toUpperCase() ?? '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className='export-footer'>
            <button
              className='export-btn'
              type='button'
              onClick={() => window.location.reload()}
            >
              Another Report
            </button>
            <button
              className='export-btn'
              type='button'
              onClick={handleExcelExport}
            >
              Download Report
            </button>
          </div>
        </div>
      )}

      {error && <div className='export-error'>{error}</div>}
    </div>
  )
}
