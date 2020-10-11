import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { connect } from 'react-redux'
import { login } from '../store/reducers/authReducer'


const Login = ({ auth, login }) => {
	const [showPassword, setShowPassword] = useState(false)
	
	const togglePassword = () => setShowPassword(!showPassword)

	const handleSubmit = (values, setSubmitting, setErrors) => {
		login(values.username, values.password)
		.catch(errors => {
			setErrors(errors.payload)
			setSubmitting(false)
		})
	}

	const SignupSchema = Yup.object().shape({
		username: Yup.string()
			.min(3, 'Username is too short!')
			.max(150, 'Username is too long!')
			.required('Username is required!'),
		password: Yup.string()
			.min(6, 'Password is too short!')
			.max(80, 'Password is too long!')
			.required('Password is required!'),
	});

	return (
		<div className='container'>
			<h1 className='text-center'>Login</h1>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<Formik
						initialValues = {{username: '', password: '', non_field_errors: ''}}
						validationSchema={SignupSchema}
						onSubmit = {(values, {setSubmitting, setErrors}) => handleSubmit(values, setSubmitting, setErrors)}
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
								<div className='input-group'>
									<Field type={showPassword ? 'text': 'password' }
										name='password'
										className={`form-control ${errors.password && touched.password ? 'is-invalid' : null}`} 
										placeholder='Password' 
									/>
									<div className='input-group-append'>
										<p 
											className='input-group-text' 
											role='button' 
											onMouseDown={togglePassword}
											onMouseUp={togglePassword}
										>
											<i className='fa fa-eye'></i>
										</p>
									</div>
								</div>
								<ErrorMessage name='password' className='text-danger' component='small' />
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
								Login
							</button>
						</Form>
						)}
					</Formik>
					<div className='mt-2'>
						<small><Link to='/password-reset'>Forgot Password?</Link></small>
					</div>
					<div className='border-top border-muted mt-2'>
						<small className='text-muted'>
							Don't have an account? <Link to='/signup'>Signup</Link>
						</small>
					</div>
				</div>
			</div>
		</div>
	)
}

export default connect(null, {login})(Login)