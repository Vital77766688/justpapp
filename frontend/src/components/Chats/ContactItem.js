import React from 'react'


const ContactItem = ({ name, pic, lastMessage, lastDate }) => {
	return (
		<div className="chat_list">
			<div className="chat_people">
				<div className="chat_img">
					<img src={pic} alt=""/>
				</div>
				<div className="chat_ib">
					<h5>{name} <span className="chat_date">{lastDate}</span></h5>
					<p>{lastMessage}</p>
				</div>
			</div>
		</div>
	)
}

export default ContactItem