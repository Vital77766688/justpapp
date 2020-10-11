import React from 'react'
import { Link } from 'react-router-dom'


const PasswordResetComplete = () => {
	return (
		<div className='container'>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<p className='mt-3'>New password has been saved. Now you can <Link to='/login'>login</Link></p>
				</div>
			</div>
		</div>
	)
}

export default PasswordResetComplete