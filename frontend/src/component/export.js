import React, { useState } from 'react'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver';
import '../css/export.css'


export default function Export() {
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [results, setResults] = useState([])
    const [aggrNumber, setAggrNumber] = useState('')

    
    
    const handleExcelExport = () => {
    const ws = XLSX.utils.json_to_sheet(results);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "SAP Data");

    const excelBuffer = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    const blob = new Blob([excelBuffer], { type: "application/octet-stream" });
    saveAs(blob, `SAP_Export_${aggrNumber}.xlsx`);
};


    const handleExportNavigate = () => {
        window.location.href = '/';
    };

    const handleClick = async (e) => {
        e.preventDefault();
        setLoading(true)
        setError(null)
        setResults([])

        const formData = new FormData();
        formData.append('aggrNumber', aggrNumber);

        try {
            const response = await fetch('http://localhost:5050/getExcel', {
                method: 'POST',
                body: formData,
            });
            const data = await response.json();
            if (!response.ok) {
                setError(data.error || 'An error occurred while processing.');
            } else {
                if (data.results) {
                    setResults(data.results);
                } else {
                    setError(data.error || "No results returned from the server")
                }
            }
        } catch (err) {
            setError(`Failed to connect to backend: ${err.message}`);
            console.error('Fetch error: ', err)
        } finally {
            setLoading(false)
        }
    };

    return (
        <div className='container'>
            {(!results || results.length === 0) ? (
                <form onSubmit={handleClick} className='app-form'>
                    <label className='aggrNumberLabel'>Agreement Number: </label>
                    <input
                        minLength={10}
                        maxLength={10}
                        type='text'
                        className='AggrNumber'
                        placeholder='Enter Agreement Number'
                        onChange={(e) => setAggrNumber(e.target.value)}
                        required
                    />
                    <div className='btn-wrapper-main'>
                    <button
                        className='btn-primary'
                        type='submit'
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : 'Export'}
                    </button>
                    
                    <button
                    className='btn-primary'
                    type='button'
                    onClick={handleExportNavigate}
                    >
                    Back
                    </button></div>
                </form>
            ) : (
                <div className="results-section">
                    <div className='adjust'>
                        <h2 className='results'>Results</h2>
                    </div>
                    <table className="results-table">
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
                        {Array.isArray(results) && results.map((res, idx) => (
                            <tr key={idx}>
                            <td>{res["Material"]?.toString().toUpperCase() ?? '-'}</td>
                            <td>{res["Short Text"]?.toString().toUpperCase() ?? '-'}</td>
                            <td>{res["Target Qty"]?.toString().toUpperCase() ?? '-'}</td>
                            <td>{res["Unit of Entry"]?.toString().toUpperCase() ?? '-'}</td>
                            <td>{res["Open Qty"]?.toString().toUpperCase() ?? '-'}</td>
                            </tr>
                        ))}
                        </tbody>

                    </table>
                    <div className='btn-wrapper'>
            <button
            className='btn-primary'
            type='button'
            onClick={() => {window.location.reload();}}
            >
            Another Report
            </button>
            <button
            className='btn-primary'
            type='button'
            onClick={handleExcelExport}>
                Download Report
            </button>
            </div>
                </div>
            )}
            {error && <div className="error-message">{error}</div>}
            
        </div>
    );
}
