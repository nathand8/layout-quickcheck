import './App.css';
import BugList from './BugList/BugList';
import SingleBug from './SingleBug/SingleBug';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

// This site has 3 pages, all of which are rendered
// dynamically in the browser (not server rendered).
//
// Although the page does not ever refresh, notice how
// React Router keeps the URL up to date as you navigate
// through the site. This preserves the browser history,
// making sure things like the back button and bookmarks
// work properly.

export default function BasicExample() {
  return (
    <Router>
      <div>
      <Navbar bg="light" expand="lg">
        <Navbar.Brand href="/">Layout QuickCheck</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Nav className="mr-auto">
          <Nav.Link href="/">BugList</Nav.Link>
        </Nav>
      </Navbar>


        <div className="App">

          {/*
            A <Switch> looks through all its children <Route>
            elements and renders the first one whose path
            matches the current URL. Use a <Switch> any time
            you have multiple routes, but you want only one
            of them to render at a time
          */}
          <Switch>
            <Route exact path="/">
              <BugList />
            </Route>
            <Route path="/bug">
              <SingleBug />
            </Route>
          </Switch>

        </div>
      </div>
    </Router>
  );
}