
function test_bug_and_report() {
  // Function recreateTheProblem() only exists in JS version with debugging tools
  if (typeof(recreateTheProblem) == "function") {
    let dimensionsDiffer = recreateTheProblem();

    if (dimensionsDiffer && dimensionsDiffer.length > 0) {

      // report the bug to the test runner
      fetch("/found")
      .finally(() => {
        finish_test(dimensionsDiffer);
      })

    } else {
      finish_test()
    }

  // If "recreateTheProblem" doesn't exist, something went wrong
  } else {
    console.error("Missing crucial function 'recreateTheProblem'. It should be provided by LQC");
  }
}

function log_bug_details(dimensionsDiffer) {

  // Add details for easier triaging
  logOutput = "\\nLQC Results:"
  for (el of dimensionsDiffer) {
    logOutput += "\\nConflicting dimensions for element " + el.element;
    logOutput += "\\n    Dimensions after reload: " + JSON.stringify(post_reload_dims);
    logOutput += "\\n    Dimensions after modify: " + JSON.stringify(post_modify_dims);
  }
  logOutput += "\\nEND of LQC Results\\n"
  try {
    window.dump(logOutput);
  } catch { }
}