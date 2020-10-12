import React from 'react'
import { connect } from 'react-redux'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { resetPasswordConfirm } from '../store/reducers/authReducer'


const PasswordResetConfirm = ({ match: { params: {uid, token} }, resetPasswordConfirm, history }) => {

	const handleResetPasswordConfirm = (values, setSubmitting, setErrors) => {
		resetPasswordConfirm(uid, token, values.new_password1, values.new_password2)
		.then(data => {
			history.push('/password-reset-complete')
		})
		.catch(errors => {
			setErrors(errors.payload)
			setSubmitting(false)
		})
	}

	const ResetPasswordConfirmSchema = Yup.object().shape({
		new_password1: Yup.string()
			.min(8, 'New password is too short!')
			.max(80, 'New password is too long!')
			.required('New password is required'),
		new_password2: Yup.string()
			.required('New password confirmation is required')
			.when("new_password1", {
				is: password => (password && password.length > 0 ? true : false),
				then: Yup.string().oneOf([Yup.ref("new_password1")], "Password doesn't match")
			})
	})

	return (
		<div className='container'>
			<h1 className='text-center'>Reset Password Confirm</h1>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<Formik
						initialValues = {{new_password1: '', new_password2: '', non_field_errors: ''}}
						validationSchema={ResetPasswordConfirmSchema}
						onSubmit = {(values, {setSubmitting, setErrors}) => handleResetPasswordConfirm(values, setSubmitting, setErrors)}
					>
						{({ errors, touched, isSubmitting }) => (
						<Form>
							<div className='form-group'>
								<Field type='password' 
									name='new_password1'
									className={`form-control ${errors.new_password1 && touched.new_password1 ? 'is-invalid' : null}`} 
									placeholder='New Password' 
								/>
								<ErrorMessage name='new_password1' className='text-danger' component='small' />
							</div>
							<div className='form-group'>
								<Field type='password' 
									name='new_password2'
									className={`form-control ${errors.new_password2 && touched.new_password2 ? 'is-invalid' : null}`} 
									placeholder='Confirm New Password' 
								/>
								<ErrorMessage name='new_password2' className='text-danger' component='small' />
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

export default connect(null, {resetPasswordConfirm})(PasswordResetConfirm)