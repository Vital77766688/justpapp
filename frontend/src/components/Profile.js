import React from 'react'
import ProfileForm from './ProfileForm'
import PasswordChangeForm from './PasswordChangeForm'


const Profile = ({ auth }) => {
return (
		<div className='container'>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<h1>Profile</h1>
					<p>welcome, {auth.user.first_name || auth.user.username}!</p>
				</div>				
			</div>
			<div className='row justify-content-center'>
				<div className='col-12-lg'>					
					<div className='row'>
						<div className='col-12-lg'>
							<h3>Update Profile</h3>
							<ProfileForm auth={auth} />
						</div>
					</div>
					<div className='row mt-3'>
						<div className='col-12-lg'>
							<h3>Change Password</h3>
							<PasswordChangeForm/>
						</div>
					</div>
				</div>
			</div>
		</div>
	)
}

export default Profile