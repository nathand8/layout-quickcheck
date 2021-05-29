import React, { useEffect, useState } from 'react';
import './SingleBug.css';
import BugDetails from '../BugDetails/BugDetails';

export default function SingleBug() {

  const bugAPI = "http://localhost:5000/api/bug/bug-report-2021-05-19-15-44-50-582456";

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