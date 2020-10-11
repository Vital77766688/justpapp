import React from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { connect } from 'react-redux'
import { resetPassword } from '../store/reducers/authReducer'


const PasswordReset = ({ auth, resetPassword, history }) => {
	
	const handleResetPassword = (values, setSubmitting, setErrors) => {
		resetPassword(values.email)
		.then(data => {
			if (data) {
				setErrors(data.payload)
				setSubmitting(false)
			} else {
				history.push('/password-reset-done')
			}
		})
	}

	const ResetPasswordSchema = Yup.object().shape({
		email: Yup.string('Please, provide a valid email address')
			.min(6, 'Email is too short!')
			.max(80, 'Email is too long!')
			.email()
			.required('Email is required!'),
	})

	return (
		<div className='container'>
			<h1 className='text-center'>Reset Password</h1>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<Formik
						initialValues = {{email: '', non_field_errors: ''}}
						validationSchema={ResetPasswordSchema}
						onSubmit = {(values, {setSubmitting, setErrors}) => handleResetPassword(values, setSubmitting, setErrors)}
					>
						{({ errors, touched, isSubmitting }) => (
						<Form>
							<div className='form-group'>
								<Field type='email' 
									name='email'
									className={`form-control ${errors.email && touched.email ? 'is-invalid' : null}`} 
									placeholder='Email' 
								/>
								<ErrorMessage name='email' className='text-danger' component='small' />
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
								Reset Password
							</button>
						</Form>
						)}
					</Formik>
				</div>
			</div>
		</div>
	)
}

export default connect(null, {resetPassword})(PasswordReset)