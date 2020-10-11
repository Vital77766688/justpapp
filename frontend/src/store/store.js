import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { appReducer } from './reducers/appReducer'
import { authReducer } from './reducers/authReducer'


const reducers = combineReducers({
	app: appReducer,
	auth: authReducer,
})

const store = createStore(reducers, applyMiddleware(thunk))

export default store
window.store = store