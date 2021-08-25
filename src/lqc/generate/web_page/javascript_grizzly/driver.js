
window.addEventListener("load", () => {
  let dimensionsDiffer = recreateTheProblem();

  if (dimensionsDiffer && dimensionsDiffer.length > 0) {
    // we found a result
    fetch("/found")
      .finally(() => {
        finish_test();
      })
  } else {
    finish_test()
  }
})