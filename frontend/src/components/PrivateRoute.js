import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import { connect } from 'react-redux'
import Spinner from './Spinner'

const PrivateRoute = ({component: Component, auth, loading, ...rest}) => (
    <Route {...rest} render={
        props => {
            if (loading) {
                return <Spinner/>
            } else if (!auth.user) {
                return <Redirect to='/login'/>
            } else {
                return <Component {...props} auth={auth}/>
            }
        }
    } />
)

const mapStateToProps = state => ({
	auth: state.auth,
    loading: state.app.isLoading,
})

export default connect(mapStateToProps)(PrivateRoute)