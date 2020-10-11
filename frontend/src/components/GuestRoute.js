import React from 'react'
import { Route, Redirect } from 'react-router-dom'
import { connect } from 'react-redux'
import Spinner from './Spinner'

const GuestRoute = ({component: Component, auth, loading, ...rest}) => (
    <Route {...rest} render={
        props => {
            if (loading) {
                return <Spinner/>
            } else if (auth.user) {
                return <Redirect to='/profile'/>
            } else {
                return <Component {...props}/>
            }
        }
    } />
)

const mapStateToProps = state => ({
    auth: state.auth,
    loading: state.app.isLoading,
})

export default connect(mapStateToProps)(GuestRoute)