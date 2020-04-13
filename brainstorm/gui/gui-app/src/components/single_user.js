import React, { Component } from 'react';
import { BrowserRouter as Router, Link } from 'react-router-dom';

const SingleUser = (props) => {
	return (
		<Link to={`/users/${props.user_id}`} className="text-decoration-none">
			<div className="m-5">
				<a className="font-weight-light h1 text-dark">
					<img className="mr-5" src={require("./user_icon_male.png")} width="100" height="100" alt="" />
					user {props.user_id}: {props.username}
				</a>
			</div>
		</Link>
	);
};

export default SingleUser;
