import React, { Component } from 'react';
import NavBar from './navbar';
import { BrowserRouter as Router, Link } from 'react-router-dom';
import RingLoader from "react-spinners/RingLoader";
import SingleUser from './single_user';
import { MDBBtn, MDBCard, MDBCardBody, MDBCardImage, MDBCardTitle, MDBCardText, MDBRow, MDBCol } from 'mdbreact';


export default class Snapshots extends Component {

	state = {user: {}, snapshots: [], loading: true }

	async componentDidMount() {
		const response1 = await fetch(`http://localhost:5000/users/${this.props.match.params.id}`);
	    const user = await response1.json();
	    const response2 = await fetch(`http://localhost:5000/users/${this.props.match.params.id}/snapshots`);
	    const snapshots = await response2.json();
	    this.setState({ user, snapshots, loading: false });
	}


	render() {
		const { user, snapshots } = this.state;

		return (
			<div>
				<NavBar />
				{ this.state.loading &&
					<div className="m-5 d-flex justify-content-center">
			    		<RingLoader
					        size={150}
					        color={"#F7C63B"}
					        loading={this.state.loading}
					        size={300}
				        />
				    </div>
				}
				{ !this.state.loading &&
					<div>
						<SingleUser user_id={user.user_id} username={user.username} />
						{
							snapshots.map((snapshot, index) => {
								return (
								 index % 5 === 0 &&
									<MDBRow className="mb-4 ml-2 mr-2">
										{snapshots.slice(index, index + 5).map(snapshot => {
											return(<SingleSnapshot user_id={user.user_id} snapshot={snapshot} /> )})
										}
									</MDBRow>
								)
							})
						}
					</div>
				}
			</div>
		);
	}
}

const SingleSnapshot = (props) => {
	return (
		
		<MDBCol>
			<Link to={`/users/${props.user_id}/snapshots/${props.snapshot.snapshot_id}`} className="text-decoration-none">
	          	<div class="card card-cascade narrower border-warning bg-transparent shadow zoom">

				  
				  <div class="view view-cascade overlay">
				    <img class="card-img-top" src={`http://localhost:5000/users/${props.user_id}/snapshots/${props.snapshot.snapshot_id}/color_image/data`}
				      alt='' />
				    <a>
				      <div class="mask rgba-white-slight"></div>
				    </a>
				  </div>

				  
				  <div class="card-body card-body-cascade">
				    <h4 class="font-weight-bold card-title text-dark"><i className="fas fa-image mr-3 ml-2" />snapshot {props.snapshot.snapshot_id}</h4>
				    <p class="card-text ml-2">{props.snapshot.datetime}</p>
				  </div>

				</div>
	        </Link>
	    </MDBCol>
		
	);
};
		

				