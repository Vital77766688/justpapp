import React, { useState } from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { connect } from 'react-redux'
import { updateProfile, sendVerificationEmail } from '../store/reducers/authReducer'


const ProfileForm = ({ auth, updateProfile, sendVerificationEmail }) => {
	const [verifyBtnDisabled, setVerifyBtnDisabled] = useState(false)

	const handleUpdateProfile = (values, setSubmitting, setErrors) => {
		updateProfile(values.username, values.email, values.first_name, values.last_name)
		.catch(errors => {
			setErrors(errors.payload)
		})
		.finally(() => setSubmitting(false))
	}

	const handleVerify = () => {
		setVerifyBtnDisabled(true)
		sendVerificationEmail()
		.finally(() => {
			setVerifyBtnDisabled(false)
		})
	}

	const ProfileSchema = Yup.object().shape({
		username: Yup.string()
			.min(3, 'Username is too short!')
			.max(150, 'Username is too long!')
			.required('Username is required!'),
		email: Yup.string('Please, provide a valid email address')
			.min(6, 'Email is too short!')
			.max(80, 'Email is too long!')
			.email()
			.required('Email is required!'),
	})

	return (
		<Formik
			initialValues = {{username: auth.user.username, 
							  email: auth.user.email,
							  first_name: auth.user.first_name,
							  last_name: auth.user.last_name,
							  non_field_errors: ''}}
			validationSchema={ProfileSchema}
			onSubmit = {(values, {setSubmitting, setErrors}) => handleUpdateProfile(values, setSubmitting, setErrors)}
		>
			{({ errors, touched, isSubmitting }) => (
			<Form>
				<div className='form-group'>
					<Field type='text' 
						name='username'
						className={`form-control ${errors.username && touched.username ? 'is-invalid' : null}`} 
						placeholder='Username' 
					/>
					<ErrorMessage name='username' className='text-danger' component='small' />
				</div>
				<div className='form-group'>
					<Field type='email' 
						name='email'
						className={`form-control ${errors.email && touched.email ? 'is-invalid' : null}`} 
						placeholder='Email'
					/>
					{!auth.user.verified ? 
						<button 
							className='btn btn-outline-danger btn-sm btn-block mt-1'
							type='button'
							onClick={handleVerify}
							disabled={verifyBtnDisabled || isSubmitting}
						>
							{verifyBtnDisabled && 
								<span 
									className="spinner-border spinner-border-sm mr-2" 
									role="status" 
									aria-hidden="true"
								></span>
							}
							Verify
						</button> :
						<small className='text-info d-block'>Email verified</small>
					}
					<ErrorMessage name='email' className='text-danger' component='small' />
				</div>
				<div className='form-group'>
					<Field type='text' 
						name='first_name'
						className={`form-control ${errors.first_name && touched.first_name ? 'is-invalid' : null}`} 
						placeholder='First Name' 
					/>
					<ErrorMessage name='first_name' className='text-danger' component='small' />
				</div>
				<div className='form-group'>
					<Field type='text' 
						name='last_name'
						className={`form-control ${errors.last_name && touched.last_name ? 'is-invalid' : null}`} 
						placeholder='Last Name' 
					/>
					<ErrorMessage name='last_name' className='text-danger' component='small' />
				</div>
				<div className='form-group'>
					<ErrorMessage name='non_field_errors' className='text-danger' component='small'/>
				</div>
				<button type='submit' 
					className='btn btn-primary btn-block'
					disabled={isSubmitting}
				>
					{isSubmitting && 
						<span 
							className="spinner-border spinner-border-sm mr-2" 
							role="status" 
							aria-hidden="true"
						></span>
					}
					Update Profile
				</button>
			</Form>
			)}
		</Formik>
	)
}

export default connect(null, {updateProfile, sendVerificationEmail})(ProfileForm)