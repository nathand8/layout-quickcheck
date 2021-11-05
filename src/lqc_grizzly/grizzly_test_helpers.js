
function test_bug_and_report() {
  // Function checkForBug() only exists in JS version with debugging tools
  if (typeof(checkForBug) == "function") {
    let dimensionsDiffer = checkForBug();

    // Mock Bug (TESTING PURPOSES ONLY)
    // dimensionsDiffer = [{
    //   "id": "one",
    //   "tag": "div",
    //   "id_tag": "one<div>",
    //   "differing_dims": ['x', 'left'],
    //   "post_modify_dims": {x: 100, left: 10},
    //   "post_reload_dims": {x: 120, left: 15}
    // }]

    if (dimensionsDiffer && dimensionsDiffer.length > 0) {

      let data = encodeURIComponent(JSON.stringify(dimensionsDiffer));

      // report the bug to the test runner
      fetch("/found?" + data)
      .finally(() => {
        finish_test(dimensionsDiffer);
      })

    } else {
      finish_test()
    }

  // If "checkForBug" doesn't exist, something went wrong
  } else {
    console.error("Missing crucial function 'checkForBug'. It should be provided by LQC");
  }
}

function log_bug_details(dimensionsDiffer) {

  // Add details for easier triaging
  logOutput = "\nLQC Results:"
  for (el of dimensionsDiffer) {
    logOutput += "\nConflicting dimensions for element " + el.id_tag;
    logOutput += "\n    Dimensions after reload: " + JSON.stringify(el.post_reload_dims);
    logOutput += "\n    Dimensions after modify: " + JSON.stringify(el.post_modify_dims);
  }
  logOutput += "\nEND of LQC Results\n"
  try {
    window.dump(logOutput);
  } catch { }
}

function bucketSize(n) {
  // The size bucketing is
  //   "small": difference < 10px
  //   "large": 10px <= difference < 100px
  //   "extreme": 100px <= difference
  if (n < 10) {
      return "small"
  } else if (n < 100) {
      return "large"
  } else {
      return "extreme"
  }
}

function result_summary(dimensionsDiffer) {
  // Outputs the differing dimensions in buckets according to bucketSize() function
  //
  // For example:
  //   dimensionsDiffer = [
  //     {
  //       id: "",
  //       tag: "body",
  //       id_tag: "UnknownID<body>",
  //       differing_dims: ['bottom', 'height'],
  //       post_modify_dims: {bottom: 100, height: 105},
  //       post_reload_dims: {bottom: 102, height: 107},
  //     },
  //     {
  //       id: "two",
  //       tag: "div",
  //       id_tag: "two<div>",
  //       differing_dims: ['y'],
  //       post_modify_dims: {y: 32},
  //       post_reload_dims: {y: 92},
  //     }
  //   ]
  // Would output
  //   "tag-body,bottom-small,height-small;tag-div,y-large"

  tagSummaries = []
  for (ob of dimensionsDiffer) {
    tag = "tag-" + ob['tag']

    obSummary = [tag]
    for (attr in ob.post_modify_dims) {
      diff = Math.abs(ob.post_modify_dims[attr] - ob.post_reload_dims[attr]);
      obSummary.push(attr + "-" + bucketSize(diff));
    }
    tagSummaries.push(obSummary.join(","));
  }

  return tagSummaries.join(";")

}