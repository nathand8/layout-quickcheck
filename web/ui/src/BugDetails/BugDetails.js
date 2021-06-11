import _ from "lodash";
import { FaCheck, FaBug, FaSignInAlt } from "react-icons/fa";
import { useState } from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ChromeBugReport from '../ChromeBugReport/ChromeBugReport';

import "./BugDetails.css";

export default function BugDetails(props) {

  const [demoVisible, setDemoVisible] = useState(false);
  const [isLinkCopied, setIsLinkCopied] = useState(false);
  const [showChromeBugReportModal, setShowChromeBugReportModal] = useState(false);
  const showChromeBugReport = () => setShowChromeBugReportModal(true);
  const closeChromeBugReport = () => setShowChromeBugReportModal(false);

  const bugLink = `/bug/${props.data.id}`;
  const absoluteBugLink = `${window.location.href}bug/${props.data.id}`;

  function toggleDemo() {
    setDemoVisible(!demoVisible);
  }

  function copyBugLink() {
    navigator.clipboard.writeText(absoluteBugLink);
    setIsLinkCopied(true);
  }

  let demoSection = <div />;
  if (demoVisible) {
    demoSection = 
      <div className="demo">
        <div className="demo-box">
          <h6>Freshly Reloaded</h6>
          <iframe title="demo_fresh" src={props.data.demo_urls.reloaded}></iframe><br />
          <a target="_blank" href={props.data.demo_urls.reloaded} rel="noreferrer">Open Separately</a>
        </div>
        <div className="demo-box">
          <h6>Dirty Changes</h6>
          <iframe title="demo_changes" src={props.data.demo_urls.dirty}></iframe><br />
          <a target="_blank" href={props.data.demo_urls.dirty} rel="noreferrer">Open Separately</a>
        </div>
      </div>      
  }

  return (
    <div>
      <div className="bug-section">
        <h4>
          {props.data.bug_type}
          <span className="demo-button" onClick={toggleDemo}>
            <FaSignInAlt />
          </span>
        </h4>
        <label>Styles</label> &mdash; <span>{_.join(props.data.styles_used, ', ')}</span>
        <div className="demo-section">
          {demoSection}
        </div>
      </div>

      <div className="bug-section">
        <h4>Variants</h4>
        {props.data.variants["Test Variant Details"].map((variant, index) => {
          return (
            <div key={index}>
              <OverlayTrigger delay={{show: 500, hide: 50}} placement="bottom"
                overlay={
                  <Tooltip>
                    {variant["is_original_variant"] ? <div>This bug was originally found on this variant</div> : ""}
                    <div><span className="capitalize">{variant["browser"]}</span> {variant["browser_version"]}</div>
                  </Tooltip>
                }>
                  <span className={variant["is_original_variant"] ? 'is_original_variant' : ''}>
                    <span className={"variant_status"}>
                      {(variant.bug_detected && <FaBug className="fail" />) || <FaCheck className="pass" />}
                    </span>
                    <label>{variant.description}</label>
                  </span>
              </OverlayTrigger>
            </div>
        )})}
      </div>

      <div className="bug-section">
        <h4>Share</h4>
        {/* Adding href property to <Button> will automatically render as an <a /> element */}
        <Button className="share-link" variant="outline-secondary" target="_blank" href={bugLink}>Open in New Tab</Button>
        <Button className="share-link" variant="outline-secondary" onClick={copyBugLink}>{isLinkCopied ? "Copied!" : "Copy Link"}</Button>
        <Button className="share-link" variant="outline-primary" onClick={showChromeBugReport}>Chrome Bug Report</Button>
      </div>

      <div>
        <Modal show={showChromeBugReportModal} onHide={closeChromeBugReport}>
          <Modal.Header closeButton>
            <Modal.Title>Chrome Bug Report</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <ChromeBugReport data={props.data}/>
          </Modal.Body>
        </Modal>
      </div>
    </div>
  );
}