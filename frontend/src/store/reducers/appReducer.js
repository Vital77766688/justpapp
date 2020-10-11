const ADD_INFO_MESSAGE = '@app-reducer/add-info-message'
const ADD_SUCCESS_MESSAGE = '@app-reducer/add-success-message'
const ADD_ERROR_MESSAGE = '@app-reducer/add-error-message'
const CLEAR_MESSAGES = '@app-reducer/clear-messages'
const START_LOADING = '@app-reducer/start-loading'
const STOP_LOADING = '@app-reducer/stop-loading'


const initialAppState = {
	infoMessages: null,
	successMessages: null,
	errorMessages: null,
	isLoading: true,
}


export const appReducer = (state=initialAppState, action) => {
	switch (action.type) {
		case ADD_INFO_MESSAGE:
			return {...state, infoMessages: action.payload}
		case ADD_SUCCESS_MESSAGE:
			return {...state, successMessages: action.payload}
		case ADD_ERROR_MESSAGE:
			return {...state, errorMessages: action.payload}
		case CLEAR_MESSAGES:
			return {...state, infoMessages: null, successMessages: null, errorMessages: null}
		case START_LOADING:
			return {...state, isLoading: true}
		case STOP_LOADING:
			return {...state, isLoading: false}
		default:
			return {...state}
	}
}


export const addInfoMessage = data => dispatch => {
	dispatch({ type: ADD_INFO_MESSAGE, payload: data })
	dispatch({ type: CLEAR_MESSAGES })
}

export const addSuccessMessage = data => dispatch => {
	dispatch({ type: ADD_SUCCESS_MESSAGE, payload: data })
	dispatch({ type: CLEAR_MESSAGES })
}

export const addErrorMessage = data => dispatch => {
	dispatch({ type: ADD_ERROR_MESSAGE, payload: data })
	dispatch({ type: CLEAR_MESSAGES })
}

export const startLoading = () => ({ type: START_LOADING })
export const stopLoading = () => ({ type: STOP_LOADING })