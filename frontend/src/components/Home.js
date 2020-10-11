import React from 'react'
import { connect } from 'react-redux'


const Home = ({ auth }) => {
	return (
		<div className='container'>
			<h1 className='text-center'>Welcome! This is home page</h1>
		</div>
	)
}

const mapStateToProps = state => ({
	auth: state.auth
})

export default connect(mapStateToProps)(Home)