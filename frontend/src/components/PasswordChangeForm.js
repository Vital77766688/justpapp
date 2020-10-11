import React from 'react'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { connect } from 'react-redux'
import { changePassword } from '../store/reducers/authReducer'


const PasswordChangeForm = ({ changePassword }) => {
	
	const handleChangePassword = (values, setSubmitting, setErrors, setValues, setTouched) => {
		changePassword(values.old_password, values.new_password1, values.new_password2)
		.then(() => {
			setValues({old_password: '', new_password1: '', new_password2: ''})
			setTouched({old_password: false, new_password1: false, new_password2: false})
		})
		.catch(errors => {
			setErrors(errors.payload)
		})
		.finally(() => setSubmitting(false))
	}

	const ChangePasswordSchema = Yup.object().shape({
		old_password: Yup.string()
			.min(8, 'Old password is too short!')
			.max(80, 'Old password is too long!')
			.required('Old password is required'),
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
		<Formik
			initialValues = {{old_password: '', 
							  new_password1: '',
							  new_password2: '',
							  non_field_errors: ''}}
			validationSchema={ChangePasswordSchema}
			onSubmit = {(values, {setSubmitting, setErrors, setValues, setTouched}) => handleChangePassword(values, setSubmitting, setErrors, setValues, setTouched)}
		>
			{({ errors, touched, isSubmitting }) => (
			<Form>
				<div className='form-group'>
					<Field type='password' 
						name='old_password'
						className={`form-control ${errors.old_password && touched.old_password ? 'is-invalid' : null}`} 
						placeholder='Old Password'
					/>
					<ErrorMessage name='old_password' className='text-danger' component='small' />
				</div>
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
					Change Password
				</button>
			</Form>
			)}
		</Formik>
	)
}

export default connect(null, {changePassword})(PasswordChangeForm)