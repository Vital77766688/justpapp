import React from 'react'
import ContactsHeader from './ContactsHeader'
import ContactItem from './ContactItem'

const Contacts = () => {

	const getContacts = () => {
		const contacts = []
		for (let i=0; i<=25; i++) {
			contacts.push({
				id: i,
				name: 'Sunil Rajput',
				lastDate: 'Dec 25',
				lastMessage: 'Test, which is a new approach to have all solutions astrology under one roof.',
				pic: 'https://ptetutorials.com/images/user-profile.png'
			})
		}
		return contacts
	}

	return (
		<div className="inbox_people">
			<ContactsHeader/>
			<div className="inbox_chat">
				{getContacts().map(contact => {
					return <ContactItem 
								key={contact.id}
								name={contact.name}
								lastDate={contact.lastDate}
								lastMessage={contact.lastMessage}
								pic={contact.pic}/>
				})}
			</div>
		</div>
	)
}

export default Contacts