import {
    BrowserRouter,
    Route,
    Routes
} from "react-router-dom";
import Purchase from './pages/Purchase';
import Restore from './pages/Restore';

const AppRoutes = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path='/purchase' element={<Purchase />} />
                <Route path='/restore' element={<Restore />} />
            </Routes>
        </BrowserRouter>
    )
}

export default AppRoutes;