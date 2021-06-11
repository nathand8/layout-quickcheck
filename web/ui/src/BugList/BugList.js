import React, { useEffect, useState } from 'react';
import _ from "lodash";

import './BugList.css';

import InputGroup from 'react-bootstrap/InputGroup';
import Button from 'react-bootstrap/Button';
import FormControl from 'react-bootstrap/FormControl';
import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip'
import BugDetails from '../BugDetails/BugDetails';
import { FaBug, FaChrome, FaExclamationTriangle, FaFirefox, FaTimes } from 'react-icons/fa';

export function displayStyleList(styles) {
  const ignore = new Set(["background-color", "min-width", "min-height"]);
  styles = _.clone(styles)
  _.remove(styles, (n) => ignore.has(n))
  return _.join(styles, ', ');
}

export function applySearch(searchStr, bugs) {
  let groups = searchStr.split(/[ ,]+/); // Split by whitespace
  let filters = groups
    .filter(group => group.length > 0)
    .map((group) => {
      if (group.startsWith("type:")) {
        return (bug) => (bug.bug_type.toLowerCase().includes(group.replace("type:", "").toLowerCase()));
      } else if (group.startsWith("seen:")) {
        return (bug) => (bug.variants["Test Variant Details"].filter(variant => variant.bug_detected).map(variant => variant.description).join(', ').toLowerCase().includes(group.replace("seen:", "").toLowerCase()))
      } else {
        return (bug) => (bug.styles_used_string.includes(group));
      }
    })
  return bugs.filter(bug => filters.every(filter => filter(bug)));
}

export default function BugList(props) {

  const bugsAPI = "/api/bugs";

  const [searchStr, setSearchStr] = useState("");
  const [bugs, setBugs] = useState([]);
  const [filteredBugs, setFilteredBugs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(bugsAPI, {method: "GET"})
      .then(res => res.json())
      .then(response => {
        setBugs(response)
        setIsLoading(false);
      })
      .catch(error => console.error(error));
  }, []); // Only run once when component loads

  useEffect(() => {
    if (bugs) {
      if (searchStr) {
        setFilteredBugs(applySearch(searchStr, bugs));
      } else {
        setFilteredBugs(bugs);
      }
    } else {
      setFilteredBugs([]);
    }
  }, [searchStr, bugs])

  return (
    <div className="BugList">

      <h2>Bug List</h2>

      <InputGroup className="search-container">
        <InputGroup.Prepend>
          <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>Clear Search</Tooltip>}>
            <Button variant="outline-secondary" onClick={e => setSearchStr("")}><FaTimes /></Button>
          </OverlayTrigger>
          <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>Page Crash Bugs</Tooltip>}>
            <Button variant="outline-secondary" onClick={e => setSearchStr(searchStr + " type:Crash")}><FaExclamationTriangle /></Button>
          </OverlayTrigger>
          <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>Underinvalidation Bugs</Tooltip>}>
            <Button variant="outline-secondary" onClick={e => setSearchStr(searchStr + " type:Invalidation")}><FaBug /></Button>
          </OverlayTrigger>
          <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>Chrome Bugs</Tooltip>}>
            <Button variant="outline-secondary" onClick={e => setSearchStr(searchStr + " seen:Chrome")}><FaChrome /></Button>
          </OverlayTrigger>
          <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>Firefox Bugs</Tooltip>}>
            <Button variant="outline-secondary" onClick={e => setSearchStr(searchStr + " seen:Firefox")}><FaFirefox /></Button>
          </OverlayTrigger>
        </InputGroup.Prepend>
        <FormControl aria-describedby="basic-addon1" value={searchStr} onChange={event => setSearchStr(event.target.value)}/>
      </InputGroup>

      {isLoading && <p>Loading Bugs...</p>}

      <Accordion defaultActiveKey="1">
        {filteredBugs.map((bug, index) => {
          let key = index + 1;
          let icon;
          let tooltip;
          if (bug.bug_type.includes("Crash")) {
            icon = <FaExclamationTriangle />;
            tooltip = "Page Crash";
          } else {
            icon = <FaBug />
            tooltip = "Under Invalidation Bug";
          }
          return (
          <Card key={index}>
            <Accordion.Toggle as={Card.Header} eventKey={key} className="clickable">
              <span className="icon">
                <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom" overlay={<Tooltip>{tooltip}</Tooltip>}>
                  {icon}
                </OverlayTrigger>
              </span> 
              {displayStyleList(bug.styles_used)}
            </Accordion.Toggle>
            <Accordion.Collapse eventKey={key}>
              <Card.Body><BugDetails data={bug}/></Card.Body>
            </Accordion.Collapse>
          </Card>
        )})}

      </Accordion>
    </div>
  );
  }