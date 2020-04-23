import React from 'react';
import ReactDOM from 'react-dom';
import '@fortawesome/fontawesome-free/css/all.min.css'; 
import 'bootstrap-css-only/css/bootstrap.min.css'; 
import 'mdbreact/dist/css/mdb.css';
import * as serviceWorker from './serviceWorker';
import "bootstrap/dist/css/bootstrap.css";
import Home from './home';
import Users from './users';
import User from './user';
import Snapshots from './snapshots'
import Snapshot from './snapshot'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';


ReactDOM.render(
  	<React.StrictMode>
  		<Router forceRefresh={true}>
        	<Switch>
        		<Route path="/" exact component={ Home }/>
        		<Route path="/users" exact component={ Users } />
        		<Route path="/users/:id" exact component={ User } />
        		<Route path="/users/:id/snapshots" exact component={ Snapshots } />
        		<Route path="/users/:id/snapshots/:sid" exact component={ Snapshot } />
        	</Switch>
      	</Router>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
