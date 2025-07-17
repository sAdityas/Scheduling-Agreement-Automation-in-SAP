import { useState } from 'react'
import '../css/insert.css'

 
export default function Insert()  {
    const [loading,setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [results, setResults] = useState([])
    const [file,setFile] = useState(null)
    const [aggrNumber, setAggrNumber] = useState('')


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

    const handleUpdateNavigate = () => {
        window.location.href = '/update'
    }

    return (
        <div className="container">
        {(!results || Object.keys(results).length === 0) ? (
        <form onSubmit={handleClick} className='app-form'>
            <input
            className='fileInput'
            type='file'
            accept='.csv'
            onChange={handleFileChange}
            required/>
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
            {loading ? 'Processing...' : 'Insert...'}
            </button>
            <button
            className='btn-primary'
            type='button'
            onClick={handleExportNavigate}
            >
            Go to Export
            </button>
            
            <button
            className='btn-primary'
            type='button'
            onClick={handleUpdateNavigate}
            >
            Update Agreement
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
            <th>Error</th>
            <th>Status</th>
            </tr>
            </thead>
            <tbody>
            {Array.isArray(results) && results.map((res, idx) => (
            <tr key={idx}>
                <td>{res.material?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.date_type?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.delivery_date?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.scheduled_quantity?.toString().toUpperCase() ?? '-'}</td>
                <td>{res.error ?? '-'}</td>
                <td className={res.error ? 'Error' : 'Completed'}>{res.error ? 'Failed' : 'Success'}</td>
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
            Upload Another File
            </button>
            
            </div>
        </div>
        )}
        {error && <div className="error-message">{error}</div>}
        </div>
    );
    }
    
    /*
    No additional code is needed here. 
    The component is already fully defined and exported above.
    If you see an error, it may be due to the misplaced $PLACEHOLDER$ or an extra closing brace.
    */