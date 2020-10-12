import React from 'react'


const ContactsHeader = () => {
	return (
		<div className="headind_srch">
			<div className="recent_heading">
				<h4>Recent</h4>
			</div>
			<div className="srch_bar">
				<div className="stylish-input-group">
					<input type="text" className="search-bar"  placeholder="Search" />
					<span className="input-group-addon">
						<button type="button">
							<i className="fa fa-search" aria-hidden="true"/>
						</button>
					</span>
				</div>
			</div>
		</div>
	)
}

export default ContactsHeader