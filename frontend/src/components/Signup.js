import React from 'react'
import { Link } from 'react-router-dom'
import { Formik, Form, Field, ErrorMessage } from 'formik'
import * as Yup from 'yup'
import { connect } from 'react-redux'
import { signup } from '../store/reducers/authReducer'


const Signup = ({ auth, signup, location }) => {

	const handleSubmit = (values, setSubmitting, setErrors) => {
		signup(values.username, values.email, values.password1, values.password2)
		.catch(errors => {
			setErrors(errors.payload)
			setSubmitting(false)
		})
	}

	const SignupSchema = Yup.object().shape({
		username: Yup.string()
			.min(3, 'Username is too short!')
			.max(150, 'Username is too long!')
			.required('Username is required'),
		email: Yup.string('Please, provide a valid email address')
			.required('Email is required')
			.email()
			.max(150, 'Email is too long'),
		password1: Yup.string()
			.min(8, 'Password is too short!')
			.max(80, 'Password is too long!')
			.required('Password is required'),
		password2: Yup.string()
			.required('Password confirmation is required')
			.when("password1", {
				is: password => (password && password.length > 0 ? true : false),
				then: Yup.string().oneOf([Yup.ref("password1")], "Password doesn't match")
			})
	})

	return (
		<div className='container'>
			<h1 className='text-center'>Signup</h1>
			<div className='row'>
				<div className='col-12-lg m-auto'>
					<Formik
						initialValues = {{username: '', email: '', password1: '', password2: '', nfe: ''}}
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
								<Field type='email' 
									name='email'
									className={`form-control ${errors.email && touched.email ? 'is-invalid' : null}`} 
									placeholder='Email' 
								/>
								<ErrorMessage name='email' className='text-danger' component='small' />
							</div>
							<div className='form-group'>
								<Field type='password' 
									name='password1'
									className={`form-control ${errors.password1 && touched.password1 ? 'is-invalid' : null}`} 
									placeholder='Password' 
								/>
								<ErrorMessage name='password1' className='text-danger' component='small' />
							</div>
							<div className='form-group'>
								<Field type='password' 
									name='password2'
									className={`form-control ${errors.password2 && touched.password2 ? 'is-invalid' : null}`} 
									placeholder='Confirm Password' 
								/>
								<ErrorMessage name='password2' className='text-danger' component='small' />
							</div>
							<div className='form-group'>
								<ErrorMessage name='nfe' className='text-danger' component='small'/>
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
								Signup
							</button>
						</Form>
						)}
					</Formik>
					<div className='border-top border-muted mt-2'>
						<small className='text-muted'>
							Already have an account? <Link to='/login'>Login</Link>
						</small>
					</div>
				</div>
			</div>
		</div>
	)
}

export default connect(null, {signup})(Signup)