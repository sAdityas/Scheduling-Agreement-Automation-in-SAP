
import Insert from './pages/insert';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Update from './pages/update';
import Export from './component/export';

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Insert />} />
        <Route path='/export' element={<Export />} />
        <Route path='/update' element={<Update />} />
      </Routes>
    </Router>
  );
}
 

export default App;