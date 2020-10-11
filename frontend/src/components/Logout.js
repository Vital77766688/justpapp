import React, { useEffect } from 'react'
import { connect } from 'react-redux'
import { logout } from '../store/reducers/authReducer'


const Logout = ({ auth, logout }) => {
	useEffect(logout, [])
	return <></>
}

export default connect(null, {logout})(Logout)