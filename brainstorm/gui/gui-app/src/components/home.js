import React, { Component } from 'react';
import { BrowserRouter as Router, Link } from 'react-router-dom';

export default class Home extends Component {
	render() {
		return (
			<div className="bg-dark p-3 mt-5">
				<h1 className="text-warning text-center pt-5 p-3 m-5 font-weight-bold display-1">BrainStorm.</h1>
				<div className="text-warning h2 font-weight-light text-center m-5">
					<p className="mt-5 mb-5 pt-5">This website exposes the information collected by the BrainStorm brain-computer interface.</p>
					<p className="mb-5 pb-5">In here you will find all the information collected on our users, including personal information and snapshots.</p>
				</div>
				<Link to='/users' className="text-decoration-none">
					<button className="d-flex justify-content-center mx-auto btn btn-outline-warning btn-xl m-5 p-3 pl-5 pr-5">View Users</button>
				</Link>
			</div>
		);
	}
}
