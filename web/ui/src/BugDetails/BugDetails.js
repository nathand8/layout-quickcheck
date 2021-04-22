import _ from "lodash";
import { FaCheckCircle, FaTimesCircle } from "react-icons/fa";

import "./BugDetails.css";

export default function BugDetails(props) {
  return (
    <div>
      <h4>{props.data.bug_type}</h4>
      <label>Styles</label> &mdash; <span>{_.join(props.data.styles_used, ', ')}</span>
      <h4>Variants</h4>
      {props.data.variants["Test Variant Details"].map((variant, index) => (
        <div key={index}>
          <span className="variant_status">{(variant.bug_detected && <FaTimesCircle className="fail" />) || <FaCheckCircle className="pass" />}</span> <label>{variant.description}</label>
        </div>
      ))}
    </div>
  );
}