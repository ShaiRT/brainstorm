import React, { Component } from 'react';
import { Link, withRouter } from 'react-router-dom';


class NavBar extends Component {

	render() {
		return (
					<nav className="navbar static-top navbar-dark bg-dark">
						<Link to="/" className="text-decoration-none">
							<a className="navbar-brand text-warning">
								<span className="ml-3 h1 font-weight-bold">BrainStorm.</span>
							</a>
						</Link>
						<Link to={this.props.match.url.substring(0, this.props.match.url.lastIndexOf('/'))}>
							<button className="font-weight-bold shadow-sm btn btn-outline-warning btn-lg p-3 pl-5 pr-5">Back</button>
						</Link>
					</nav>
				);
	}
};

export default withRouter(NavBar);
