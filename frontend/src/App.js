import React, { useEffect } from 'react';
import './App.css';
import { Switch, Route } from 'react-router-dom'
import { connect } from 'react-redux'
import { me } from './store/reducers/authReducer'
import PrivateRoute from './components/PrivateRoute'
import GuestRoute from './components/GuestRoute'
import NotFound404 from './components/NotFound404'
import Alerts from './components/Alerts'
import Header from './components/Header'
import Home from './components/Home'
import Profile from './components/Profile'
import Login from './components/Login'
import Signup from './components/Signup'
import Logout from './components/Logout'
import VerifyEmail from './components/VerifyEmail'
import PasswordReset from './components/PasswordReset'
import PasswordResetDone from './components/PasswordResetDone'
import PasswordResetConfirm from './components/PasswordResetConfirm'
import PasswordResetComplete from './components/PasswordResetComplete'


function App({ me }) {
    useEffect(me, [])
    return (
        <div className="App">
            <Header/>
            <Alerts/>
            <Switch>
                <GuestRoute path='/login' component={Login}/>
                <GuestRoute path='/signup' component={Signup}/>
                <PrivateRoute path='/profile' component={Profile}/>
                <PrivateRoute path='/logout' component={Logout}/>
                <Route path='/verify-email/:key' component={VerifyEmail}/>
                <Route path='/password-reset' component={PasswordReset}/>
                <Route path='/password-reset-done' component={PasswordResetDone}/>
                <Route path='/password-reset-confirm/:uid/:token' component={PasswordResetConfirm}/>
                <Route path='/password-reset-complete' component={PasswordResetComplete}/>
                <Route exact path='/' component={Home}/>
                <Route path='*' component={NotFound404}/>
            </Switch>
        </div>
    )
}

export default connect(null, {me})(App)
