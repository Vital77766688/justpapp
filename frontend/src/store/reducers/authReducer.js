import axios from 'axios'
import { addSuccessMessage, 
		 addInfoMessage, 
		 addErrorMessage,
		 startLoading,
		 stopLoading, 
} from './appReducer'


const ME_SUCCESS = '@auth-reducer/me-success'
const ME_FAILURE = '@auth-reducer/me-failure'

const LOGIN_SUCCESS = '@auth-reducer/login-success'
const LOGIN_FAILURE = '@auth-reducer/login-failure'

const SIGNUP_SUCCESS = '@auth-reducer/signup-success'
const SIGNUP_FAILURE = '@auth-reducer/signup-failure'

const LOGOUT = '@auth-reducer/logout'

const UPDATE_PROFILE_SUCCESS = '@auth-reducer/update-profile-success'
const UPDATE_PROFILE_FAILURE = '@auth-reducer/update-profile-failure'

const CHANGE_PASSWORD_SUCCESS = '@auth-reducer/change-password-success'
const CHANGE_PASSWORD_FAILURE = '@auth-reducer/change-password-failure'

const RESET_PASSWORD_SUCCESS = '@auth-reducer/reset-password-success'
const RESET_PASSWORD_FAILURE = '@auth-reducer/reset-password-failure'

const RESET_PASSWORD_CONFIRM_FAILURE = '@auth-reducer/reset-password-confirm-failure'

const VERIFY_EMAIL_SUCCESS = '@auth-reducer/verify-email-success'


const normalizeError = errors => (errors.response ? errors.response.data : {non_field_errors: errors.message}) 


const authInitialState = {
	token: localStorage.getItem('auth-token'),
	user: null,
}

export const authReducer = (state=authInitialState, action) => {
	switch (action.type) {
		case ME_SUCCESS:
		case UPDATE_PROFILE_SUCCESS:
			return {...state, user: action.payload}
		case LOGIN_SUCCESS:
		case SIGNUP_SUCCESS:
			localStorage.setItem('auth-token', action.payload.token)
			return {...state, 
				token: action.payload.token, 
				user: action.payload.user,
			}
		case VERIFY_EMAIL_SUCCESS:
			if (state.user) {
				return {...state, user: {...state.user, verified: true}}
			} 
			return {...state}
		case ME_FAILURE:
		case LOGIN_FAILURE:
		case SIGNUP_FAILURE:
			let token = state.token
			if (action.payload && action.payload.detail && action.payload.detail === 'Invalid token.') {
				localStorage.removeItem('auth-token')
				token = null
			}
			return {...state, token: token, user: null}
		case LOGOUT:
			localStorage.removeItem('auth-token')
			return {...state, token: null, user: null}
		default:
			return {...state}
	}
}


export const me = () => dispatch => {
	const token = localStorage.getItem('auth-token')
	if (token) {
		dispatch(startLoading())
		axios.get('/auth/user/', {
			headers: {
				'Authorization': `Token ${token}`
			}
		})
		.then(response => {
			dispatch({ type: ME_SUCCESS, payload: response.data })
		})
		.catch(errors => {
			dispatch({ type: ME_FAILURE, payload: normalizeError(errors) })
			dispatch(addErrorMessage(normalizeError(errors)))
		})
		.finally(() => dispatch(stopLoading()))
	} else {
		dispatch({ type: ME_FAILURE })
		dispatch(stopLoading())
	}
}


export const login = (username, password) => dispatch => {
	return axios.post('/auth/login/', {username, password})
	.then(response => {
		dispatch({ type: LOGIN_SUCCESS, payload: {token: response.data.key, user: response.data.user} })
	})
	.catch(errors => {
		throw dispatch({ type: LOGIN_FAILURE, payload: normalizeError(errors) })
	})
}


export const signup = (username, email, password1, password2) => dispatch => {
    return axios.post('/auth/registration/', {
    	username,
    	email,
    	password1,
    	password2,
    })
    .then(response => {
    	dispatch({ type: SIGNUP_SUCCESS, payload: {token: response.data.key, user: response.data.user} })
    	dispatch(addInfoMessage('You have successfully signup! Check your email for activation link'))
    })
    .catch(errors => {
		throw dispatch({ type: SIGNUP_FAILURE, payload: normalizeError(errors) })
    })
}


export const logout = () => dispatch => {
	dispatch(startLoading())
	axios.post('/auth/logout/', null, {
		headers: {
			'Authorization': `Token ${localStorage.getItem('auth-token')}`
		}
	})
	.then(response => {
		dispatch({ type: LOGOUT })
		dispatch(addSuccessMessage(response.data))
	})
	.catch(errors => {
		dispatch({ type: LOGOUT })	
	})
	.finally(() => dispatch(stopLoading()))
}

export const updateProfile = (username, email, first_name, last_name) => dispatch => {
	return axios.put('/auth/user/', {
		username,
		email,
		first_name,
		last_name,
	}, {
		headers: {
			'Authorization': `Token ${localStorage.getItem('auth-token')}`
		}
	})
	.then(response => {
		dispatch({ type: UPDATE_PROFILE_SUCCESS, payload: response.data })
		dispatch(addSuccessMessage('Profile updated. If you changed your email address, please check it for an activation link.'))
	})
	.catch(errors => {
		throw dispatch({ type: UPDATE_PROFILE_FAILURE, payload: normalizeError(errors) })
	})
}

export const changePassword = (old_password, new_password1, new_password2) => dispatch => {
	return axios.post('/auth/password/change/', {
		old_password,
		new_password1,
		new_password2
	}, {
		headers : {
			'Authorization': `Token ${localStorage.getItem('auth-token')}`
		}
	})
	.then(response => {
		dispatch({ type: CHANGE_PASSWORD_SUCCESS })
		dispatch(addSuccessMessage(response.data))
	})
	.catch(errors => {
		throw dispatch({ type: CHANGE_PASSWORD_FAILURE, payload: normalizeError(errors) })
	})
}

export const resetPassword = email => dispatch => {
	return axios.post('/auth/password/reset/', {email})
	.then(response => {
		dispatch({ type: RESET_PASSWORD_SUCCESS })
		dispatch(addInfoMessage('Reset link was sent to your email'))
	})
	.catch(errors => {
		throw dispatch({ type: RESET_PASSWORD_FAILURE, payload: normalizeError(errors) })	
	})
}

export const resetPasswordConfirm = (uid, token, new_password1, new_password2) => dispatch => {
	return axios.post('/auth/password/reset/confirm/', {
		uid,
		token,
		new_password1,
		new_password2,
	})
	.then(response => {
		dispatch(addSuccessMessage(response.data))
	})
	.catch(errors => {
		throw dispatch({ type: RESET_PASSWORD_CONFIRM_FAILURE, payload: normalizeError(errors) })
	})
}

export const sendVerificationEmail = () => dispatch => {
	return axios.post('/auth/resend-confirmation-email/', null, {
		headers: {
			'Authorization': `Token ${localStorage.getItem('auth-token')}`
		}
	})
	.then(response => {
		dispatch(addInfoMessage(response.data))
	})
	.catch(errors => {
		dispatch(addErrorMessage(normalizeError(errors)))	
	})
}

export const verifyEmail = key => dispatch => {
	dispatch(startLoading())
	return axios.post('/auth/registration/verify-email/', {key})
	.then(response => {
		dispatch({ type: VERIFY_EMAIL_SUCCESS })
		dispatch(addSuccessMessage(response.data))
	})
	.catch(errors => {
		dispatch(addErrorMessage(normalizeError(errors)))	
	})
	.finally(() => dispatch(stopLoading()))
}
