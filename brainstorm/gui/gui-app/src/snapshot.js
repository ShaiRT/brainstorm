import React, { Component } from 'react';
import NavBar from './navbar'
import { Link, withRouter } from 'react-router-dom';
import RingLoader from "react-spinners/RingLoader";
import SingleUser from './single_user';

class Snapshot extends Component {

	state = {user: {}, 
			 snapshot: {}, 
			 image_src: `${window.api_url}/users/${this.props.match.params.id}/snapshots/${this.props.match.params.sid}/color_image/data`, 
			 loading: true};

	async componentDidMount() {
	    await this.getData();
	    setTimeout(() => {this.setState({ loading: false });}, 200);
	}

	getData = async () => {
		const response1 = await fetch(`${window.api_url}/users/${this.props.match.params.id}`);
	    const user = await response1.json();
	    const response2 = await fetch(`${window.api_url}/users/${this.props.match.params.id}/snapshots/${this.props.match.params.sid}`);
	    const snapshot = await response2.json();
	   	snapshot.available_results.map(async (result) => {
	   		var response = await fetch(`${window.api_url}/users/${this.props.match.params.id}/snapshots/${this.props.match.params.sid}/${result}`);
	    	var data = await response.json();
	   		snapshot[result] = data;
	   	});
	   	if (snapshot.feelings === undefined) {
	   		snapshot.feelings = {};
	   	}
	   	if (snapshot.pose === undefined) {
	   		snapshot.pose = {translation: {}, rotation: {}};
	   	}
	    this.setState({ user, snapshot });
	}

	handleMouseOver = () => {
    	this.setState({
      		image_src: `${window.api_url}/users/${this.props.match.params.id}/snapshots/${this.props.match.params.sid}/depth_image/data`
    	});
  	}


   	handleMouseOut = () => {
    	this.setState({
      		image_src: `${window.api_url}/users/${this.props.match.params.id}/snapshots/${this.props.match.params.sid}/color_image/data`
    	});
  	}

  	getHSL = num => {
  		return(`hsl(${(num + 1) * 60}, 95%, 65%)`);
  	}

  	getPercent = num => {
  		if (num === undefined) {
  			return ('-----');
  		}
  		num = (num + 1) / 2;
  		return (`${Number(num * 100).toFixed(1)}%`);
  	}

	render() {
		const { user, snapshot } = this.state;
		console.log(this.state.loading, snapshot.pose);

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
			    		<a className="row">
			    			<div className="col-md-5">
			    				<SingleUser className="col-md-6" user_id={user.user_id} username={user.username} />
								<img className="p-3 ml-5 shadow" onMouseOver={this.handleMouseOver} onMouseOut={this.handleMouseOut} src={this.state.image_src} width="690" height="440" alt="" />
								<Link to={`/users/${user.user_id}/snapshots/${snapshot.snapshot_id - 1}`} className="text-decoration-none">
									<button className="float-left font-weight-bold btn btn-outline-warning btn-lg m-5 p-3 pl-5 pr-5">Previous</button>
								</Link>
							</div>
							<div className="col-md-5 m-1 mt-0 ml-5 pl-5 p-1 pt-0">
								<h1 className="mt-5 pt-5 mb-1 font-weight-bold display-1">Snapshot {snapshot.snapshot_id}</h1>
								<h3 className="ml-4 mt-2">Date: {snapshot.datetime}</h3>
								<div className="text-secondary ml-2">
									<h3 className="m-3 mt-4">Pose</h3>
									<div className="ml-3">
										<h4 className="m-3 pl-3">Translation: ({Number(snapshot.pose.translation.x).toFixed(3)}, {Number(snapshot.pose.translation.y).toFixed(3)}, {Number(snapshot.pose.translation.z).toFixed(3)})</h4>
										<h4 className="m-3 pl-3">Rotation: ({Number(snapshot.pose.rotation.x).toFixed(3)}, {Number(snapshot.pose.rotation.y).toFixed(3)}, {Number(snapshot.pose.rotation.z).toFixed(3)}, {Number(snapshot.pose.rotation.w).toFixed(3)})</h4>
									</div>
									<h3 className="m-3 mt-4">Feelings</h3>
									<div className="ml-3 col-md-12 text-dark">
										<div className="row ml-3">
											<h4 className="col badge-pill m-2 p-1 pt-3 pb-3 shadow-sm" style={{backgroundColor: this.getHSL(snapshot.feelings.happiness)}}><i className="fas fa-grin-beam mr-4 pl-4" />Happiness: {this.getPercent(snapshot.feelings.happiness)}</h4>
											<h4 className="col badge-pill m-2 p-1 pt-3 pb-3 shadow-sm" style={{backgroundColor: this.getHSL(-snapshot.feelings.hunger)}}><i className="fas fa-hamburger mr-4 pl-4" />Hunger: {this.getPercent(snapshot.feelings.hunger)}</h4>
										</div>
										<div className="row ml-3">
											<h4 className="col badge-pill m-2 p-1 pt-3 pb-3 shadow-sm" style={{backgroundColor: this.getHSL(-snapshot.feelings.thirst)}}><i className="fas fa-coffee mr-4 pl-4" />Thirst: {this.getPercent(snapshot.feelings.thirst)}</h4>
											<h4 className="col badge-pill m-2 p-1 pt-3 pb-3 shadow-sm" style={{backgroundColor: this.getHSL(-snapshot.feelings.exhaustion)}}><i className="fas fa-battery-half mr-4 pl-4" />Exhaustion: {this.getPercent(snapshot.feelings.exhaustion)}</h4>
										</div>
									</div>
								</div>
							</div>
							<Link to={`/users/${user.user_id}/snapshots/${snapshot.snapshot_id + 1}`} className="align-self-end text-decoration-none">
								<button className="float-right font-weight-bold btn btn-outline-warning btn-lg m-5 p-3 pl-5 pr-5">Next</button>
							</Link>
						</a>
					</div>
				}
			</div>
		);
	}
}

export default withRouter(Snapshot);
