
import Insert from './pages/insert';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Export from './component/export';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Insert />} />
        <Route path='/export' element={<Export />} />
      </Routes>
    </Router>
  );
}
 

export default App;