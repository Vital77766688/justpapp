import React, { useEffect } from 'react'
import { connect } from 'react-redux'
import { verifyEmail } from '../store/reducers/authReducer'
import Spinner from './Spinner'


const VerifyEmail = ({ match: { params: {key} }, verifyEmail, history }) => {

	useEffect(() => {
		verifyEmail(key)
		.then(() => {
			history.push('/profile')
		})
	}, [key, verifyEmail, history])

	return <Spinner/>

}

export default connect(null, {verifyEmail})(VerifyEmail)