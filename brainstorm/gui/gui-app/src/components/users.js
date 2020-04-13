import React, { Component } from 'react';
import NavBar from './navbar';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import SingleUser from './single_user';

export default class Users extends Component {

	state = {users: []}

	async componentDidMount() {
	    const response = await fetch('http://localhost:5000/users');
	    const data = await response.json();
	    this.setState({ users: data });
	}

	render() {
		const { users } = this.state;

		return (
			<div>
				<NavBar />
				<ul className="list-group list-group-flush">
					{users.map(user => 
						<li className="list-group-item list-group-item-action list-group-item-warning">
							<SingleUser user_id={user.user_id} username={user.username} />
						</li>
					)}
				</ul>
			</div>
		);
	}
}
