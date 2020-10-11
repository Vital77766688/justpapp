import React, { useEffect } from 'react'
import { withAlert } from 'react-alert'
import { connect } from 'react-redux'


const Alerts = ({ errorMessages, successMessages, infoMessages, alert }) => {

	useEffect(() => {
		if (errorMessages) {
			if (typeof errorMessages === 'object') {
				for (let field in errorMessages) {
					if (typeof errorMessages[field] === 'object') {						
						for (let message of errorMessages[field]) {
							alert.error(message)
						}
					} else {
						alert.error(errorMessages[field])
					}
				}
			} else {
				alert.error(errorMessages)
			}
		} else if (successMessages) {
			if (typeof successMessages === 'object') {
				for (let field in successMessages) {
					if (typeof successMessages[field] === 'object') {						
						for (let message of successMessages[field]) {
							alert.success(message)
						}
					} else {
						alert.success(successMessages[field])
					}
				}
			} else {
				alert.success(successMessages)
			}
		} else if (infoMessages) {
			if (typeof infoMessages === 'object') {
				for (let field in infoMessages) {
					if (typeof infoMessages[field] === 'object') {						
						for (let message of infoMessages[field]) {
							alert.info(message)
						}
					} else {
						alert.info(infoMessages[field])
					}
				}
			} else {
				alert.info(infoMessages)
			}
		}
	}, [errorMessages, successMessages, infoMessages, alert])

	return <></>
}

const mapStateToProps = state => ({
	infoMessages: state.app.infoMessages,
	successMessages: state.app.successMessages,
	errors: state.app.errorMessages,
})

export default connect(mapStateToProps)(withAlert()(Alerts))