import React, { useEffect, useState } from 'react';
import { useParams } from "react-router-dom";
import './SingleBug.css';
import BugDetails from '../BugDetails/BugDetails';

export default function SingleBug() {

  let {bug_id} = useParams();

  const bugAPI = `/api/bug/${bug_id}`;

  const [bug, setBug] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetch(bugAPI, {method: "GET"})
      .then(res => res.json())
      .then(response => {
        setBug(response)
        setIsLoading(false);
      })
      .catch(error => console.error(error));
  }, []); // Only run once when component loads

  if (isLoading) {
    return <p>Loading Bugs...</p>
  } else {
    return (
      <div>
        <h2>Single Bug</h2>
        <BugDetails data={bug}/>
      </div>
    );
  }

}