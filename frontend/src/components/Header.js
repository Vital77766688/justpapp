import React from 'react'
import { Link } from 'react-router-dom'
import { connect } from 'react-redux'


const Header = ({ auth, location }) => {
	const authLinks = (
		<ul className="navbar-nav">
			<li className="nav-item dropdown">
		        <Link className="nav-link dropdown-toggle" to='/' id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
		          {auth.user && auth.user.email}
		        </Link>
		        <div className="dropdown-menu" aria-labelledby="navbarDropdown">
		        	<Link className="dropdown-item" to='/profile'>Profile</Link>
		        	<div className="dropdown-divider"></div>
		        	<Link className="dropdown-item" to='/logout'>Logout</Link>
		        </div>
		      </li>
		</ul>
	)


	const guestLinks = (
		<ul className="navbar-nav">
			<li className="nav-item">
				<Link className="nav-link" to='/login'>Login</Link>
			</li>
			<li className="nav-item">
				<Link className="nav-link" to='/signup'>Signup</Link>
			</li>
		</ul>
	)

	return (
		<header>
			<nav className="navbar navbar-expand-lg navbar-light bg-light">
				<div className="container">
					<Link className="navbar-brand" to="/">Auth System</Link>
					<button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
						<span className="navbar-toggler-icon"></span>
					</button>
					<div className="collapse navbar-collapse" id="navbarSupportedContent">
						<ul className="navbar-nav mr-auto">
							<li className="nav-item">
								<Link className="nav-link" to='/'>Home</Link>
							</li>
							<li className="nav-item">
								<Link className="nav-link" to='/chats'>Chats</Link>
							</li>
						</ul>
						{auth.user ? authLinks : guestLinks}
					</div>
				</div>
			</nav>
		</header>
	)
}

const mapStateToProps = state => ({
	auth: state.auth
})

export default connect(mapStateToProps)(Header)