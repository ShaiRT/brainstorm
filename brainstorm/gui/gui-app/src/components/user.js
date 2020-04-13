import React, { Component } from 'react';
import NavBar from './navbar'
import { BrowserRouter as Router, Link } from 'react-router-dom';

export default class User extends Component {

	state = {user: {}}

	async componentDidMount() {
	    const response = await fetch(`http://localhost:5000/users/${this.props.match.params.id}`);
	    const data = await response.json();
	    this.setState({ user: data });
	}

	render() {
		const { user } = this.state;

		return (
			<div>
				<NavBar />
				<a className="row">
					<div className="col-md-3">
						<img className="p-5 m-5" src={require(`./user_icon_male.png`)} width="450" height="450" alt="" />
					</div>
					<div className="col-md-5 m-5 p-5">
						<h1 className="mt-2 pt-2 mb-5 font-weight-bold display-1">{user.username}</h1>
						<div className="text-secondary">
							<h3 className="m-3">User ID: {user.user_id}</h3>
							<h3 className="m-3">Birthday: {user.birthday}</h3>
							<h3 className="m-3">Gender: {user.gender}</h3>
						</div>
					</div>
				</a>
				<Link to={`/users/${user.user_id}/snapshots`} className="text-decoration-none row">
					<button className="font-weight-bold shadow-sm mx-auto col-md-3 btn btn-outline-warning btn-lg p-3">View Snapshots</button>
				</Link>
			</div>
		);
	}
}
