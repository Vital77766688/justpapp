import React from 'react'


const IncomingMessage = ({ user, messageText, messageDate }) => {
	return (
		<div className="incoming_msg">
			<div className="incoming_msg_img">
				<img src={user.pic} alt={user.username}/> 
			</div>
			<div className="received_msg">
				<div className="received_withd_msg">
					<p>{messageText}</p>
					<span className="time_date">{messageDate}</span>
				</div>
			</div>
		</div>
	)
}

export default IncomingMessage