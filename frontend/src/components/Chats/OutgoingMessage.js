import React from 'react'


const OutgoingMessage = ({ messageText, messageDate }) => {
	return (
		<div className="outgoing_msg">
			<div className="sent_msg">
				<p>{messageText}</p>
				<span className="time_date">{messageDate}</span>
			</div>
		</div>
	)
}

export default OutgoingMessage