import { useState } from 'react'
import '../css/insert.css'

 
export default function Insert()  {
    const [loading,setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [results, setResults] = useState([])
    const [file,setFile] = useState(null)
    const [aggrNumber, setAggrNumber] = useState('')
    const [finalStatus, setFinalStatus] = useState('')


    const handleFileChange = (e) =>{
        setFile(e.target.files[0])
    }
    const handleClick = async(e) =>{
        e.preventDefault();
        setLoading(true)
        setError(null)
        setResults([])

        const formData = new FormData();
        if(!file){
        setError("Please select an Excel/CSV file.");
        setLoading(false);
        return;
        }
        formData.append('file',file)
        formData.append('aggrNumber',aggrNumber)


        try{
        const response = await fetch('http://127.0.0.1:5050/main' , {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        console.log(data)
        setFinalStatus(data.status)
        if(!response.ok){
            setError(data.error || 'An error occurred while processing.');
        }else{
            if(data.results){
            setResults(data.results);
            }else{
            setError(data.error || "No results returned from the server")
            }
        }
        }catch (err){
        setError(`Failed to connect to backend: ${err.message}`);
        console.error('Fetch error: ',err)
        }finally {
        setLoading(false)
        }
    };

    // Add navigation to /export
    const handleExportNavigate = () => {
        window.location.href = '/export';
    };

    return (
        <div className="insert-container">
            <div className='main-container'>
                <div className='title'>
                    <h2>Insert New Schedule</h2>
                </div>
                <hr className='breaker'/>
        {(!results || Object.keys(results).length === 0) ? (
        <form onSubmit={handleClick} className='app-form'>
            <input
            className='fileInput'
            type='file'
            accept='.csv'
            onChange={handleFileChange}
            required/>
            <div className='aggrNumber-container'>
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
            </div>
            <div className='button-container'>
            <button
            className={`${loading ? 'btn-primary-loading' : 'btn-primary'}`}
            type='submit'
            disabled={loading}
            >
            {loading ? (<span className="loader-container">Processing
                <span className="loader">.</span>
                <span className="loader">.</span>
                <span className="loader">.</span>
            </span>) : ('Insert')}
            </button>
            <button
            className={`${loading ? 'btn-primary-loading' : 'btn-primary'}`}
            type='button'
            onClick={handleExportNavigate}
            disabled={loading}
            >
            Go to Export
            </button>
            </div>  
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
            <th>Date Type</th>
            <th>Delivery Date</th>
            <th>Scheduled Quantity</th>
            <th>Status</th>
            <th>Final Status</th>
            </tr>
            </thead>
            <tbody>
            {Array.isArray(results) && results.map((res, idx) => (
            <tr key={idx}>
                <td>{res.material?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.date_type?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.delivery_date?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.scheduled_quantity?.toString().toUpperCase() ?? '-'}</td>
                {res.updated === null ?
                <td>{res.error }</td>
                :
                <td>{res.updated?.status === 'failed' ? res.updated?.result : "Previous Schedulee Closed with GRN Qty " + res.updated.updatedResult?.GRN }</td>
                }
                <td>{finalStatus ?? '-'}</td>
                
            </tr>
            ))}
            </tbody>
            </table>
            <div className='btn-wrapper'>
            <button
            className='btn-primary-upld'
            type='button'
            onClick={() => {window.location.reload();}}
            >
            Upload Another File
            </button>
            
            </div>
        </div>
        )}
        {error && <div className="error-message">{error}</div>}
            </div>
        </div>
    );
    }