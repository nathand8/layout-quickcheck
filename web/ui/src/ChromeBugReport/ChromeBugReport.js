import { useState } from 'react';
import Button from 'react-bootstrap/Button';

import "./ChromeBugReport.css";


export default function ChromeBugReport(props) {

  const variants = props.data.variants["Test Variant Details"];
  const originalVariant = variants.find((v) => v.is_original_variant);

  const initialReportText = `Chrome Version: ${originalVariant.browser} ${originalVariant.browser_version}

Complete List of Browser Variants Tested:
${variants.map((v) => {
    const result = v.bug_detected ? 'FAIL' : 'OK';
    return `${result} - ${v.description} (${v.browser} ${v.browser_version})\n`;
  }).join("")}

Steps to Reproduce:

1. Open the attached HTML File
2. Run the JS function simpleRecreate() 

Expected Behavior:

The attached file follows a few simple steps:
- Initial HTML/CSS is loaded on the page
- CSS styles are changed and the elements are measured (measure #1)
- All elements are reloaded (including the CSS changes) and the elements are measured again (measure #2)
- The measurements from #1 and #2 should match. 

What happens instead?
- The measurements from #1 and #2 don't match. This is likely an Under-Invalidation bug.


This bug is generated from Layout QuickCheck (https://github.com/nathand8/layout-quickcheck). 
Internal reference '${props.data.id}'. 

Feel free to contact for more details on Layout QuickCheck or to offer suggestions on more effective bug reporting.
`
  

  const [isCopied, setIsCopied] = useState(false);
  const [reportText, setReportText] = useState(initialReportText);

  const textChanged = (event) => {
    setReportText(event.target.value);
    setIsCopied(false);
  }

  function copyText() {
    navigator.clipboard.writeText(reportText);
    setIsCopied(true);
  }

  return (
      <div>

        <div className="report-text">
            <textarea className="report-textarea" value={reportText} onChange={textChanged} />
        </div>

        <div>
          Remember to download files and attach them to bug reports.
        </div>

        <div className="links-section">
          <Button variant="outline-primary" onClick={copyText}>{isCopied ? "Copied!" : "Copy Text"}</Button>
        </div>
      </div>
  );
}