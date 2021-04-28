import React, { useEffect, useState } from 'react';
import _ from "lodash";

import './BugList.css';

import Accordion from 'react-bootstrap/Accordion';
import Card from 'react-bootstrap/Card';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip'
import BugDetails from '../BugDetails/BugDetails';
import { FaBug, FaExclamationTriangle } from 'react-icons/fa';

export function displayStyleList(styles) {
  const ignore = new Set(["background-color", "min-width", "min-height"]);
  styles = _.clone(styles)
  _.remove(styles, (n) => ignore.has(n))
  return _.join(styles, ', ');
}

export default function BugList(props) {

  const bugsAPI = "http://localhost:5000/bugs";

  const [bugs, setBugs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(bugsAPI, {method: "GET"})
      .then(res => res.json())
      .then(response => {
        setBugs(response)
        setIsLoading(false);
        console.log(response);
      })
      .catch(error => console.error(error));
  }, []); // Only run once when component loads

  return (
    <div className="BugList">
      {isLoading && <p>Loading Bugs...</p>}
      <Accordion defaultActiveKey="1">

        {bugs.map((bug, index) => {
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