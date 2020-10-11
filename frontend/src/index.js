import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { BrowserRouter } from 'react-router-dom'
import { Provider } from 'react-redux'
import { positions, Provider as AlertProvider } from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'
import store from './store/store'
import App from './App';


const options = {
	position: positions.TOP_RIGHT,
	timeout: 5000,
}

ReactDOM.render(
  <React.StrictMode>
	<BrowserRouter>
		<Provider store={store}>
			<AlertProvider template={AlertTemplate} {...options}>
		    	<App />
		    </AlertProvider>
	    </Provider>
	</BrowserRouter>
  </React.StrictMode>,
  document.getElementById('root')
);