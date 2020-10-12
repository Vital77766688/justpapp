import React from 'react'
import Contacts from './Contacts'
import Messages from './Messages'


const Chats = () => {
	return (
    <>
        <div className="messaging">
            <div className="inbox_msg">
                <Contacts/>
                <Messages/>
            </div>    
        </div>
    </>
	)
}

export default Chats