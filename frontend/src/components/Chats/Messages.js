import React from 'react'
import MessageInput from './MessageInput'
import IncomingMessage from './IncomingMessage'
import OutgoingMessage from './OutgoingMessage'


const Messages = () => {

	const user = {
		name: 'Sunil Rajput',
		lastDate: 'Dec 25',
		lastMessage: 'Test, which is a new approach to have all solutions astrology under one roof.',
		pic: 'https://ptetutorials.com/images/user-profile.png'
	}

	const getMessages = () => {
		const messages = []
		for (let i=0; i<25; i++) {
			const isIncoming = Math.random() > 0.5
			messages.push({
				id: i,
				isIncoming: isIncoming,
				user: user,
				messageText: 'Test which is a new approach to have all solutions. Test which is a new approach to have all solutions',
				messageDate: '11:01 AM    |    June 9',
			})
		}
		return messages
	}

	return (
		<div className="mesgs">
			<div className="msg_history">
				{getMessages().map(message => {
					if (message.isIncoming) {
						return <IncomingMessage 
									key={message.id}
									user={message.user}
									messageText={message.messageText}
									messageDate={message.messageDate}
								/>
					} else {
						return <OutgoingMessage
									key={message.id}
									messageText={message.messageText}
									messageDate={message.messageDate}
								/>
					}
				})}
			</div>
			<MessageInput/>
		</div>
	)
}

export default Messages