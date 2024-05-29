import React from 'react'
import { BrowserRouter, Route } from 'react-router-dom'

import Login from './pages/Login'
import Register from './pages/Register'
import UserPage from './pages/UserPage'
import HomePage from './pages/HomePage'

const App = () => {
  return (
	  <div>
		<BrowserRouter>
				<Route path="/" exact component={HomePage} />
				<Route path="/login" exact component={Login} />
				<Route path="/register" exact component={Register} />
				<Route path="/userpage" exact component={UserPage} />
		</BrowserRouter>
	</div>
	
  );
}

export default App;
