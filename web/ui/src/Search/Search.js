function typeMatch(bug, s, reverse = false) {
  let result = bug.bug_type.toLowerCase().includes(s.toLowerCase());
  return reverse ? !result : result;
}

function variantDescriptionMatch(bug, s, reverse = false) {
  return bug.variants["Test Variant Details"]
          .filter(v => reverse ? !v.bug_detected : v.bug_detected)
          .map(variant => variant.description.replace(/\s+/g, '')) // remove all whitespace
          .join(', ')
          .toLowerCase()
          .includes(s.toLowerCase());
}

function styleContains(bug, s, reverse = false) {
  let result = bug.styles_used_string.toLowerCase().includes(s.toLowerCase());
  return reverse ? !result : result;
}

function variantBrowserVersionMatch(bug, s, reverse = false) {
  return bug.variants["Test Variant Details"]
          .filter(v => reverse ? !v.bug_detected : v.bug_detected)
          .map(variant => variant.browser_version)
          .join(', ')
          .toLowerCase()
          .includes(s.toLowerCase());
}


export function applySearch(searchStr, bugs) {
  let groups = searchStr.split(/[ ,]+/); // Split by whitespace
  let filters = groups
    .filter(group => group.length > 0)
    .map((group) => {

      if (group.startsWith("type:")) {
        return (bug) => typeMatch(bug, group.replace("type:", ""));
      } else if (group.startsWith("!type:")) {
        return (bug) => typeMatch(bug, group.replace("!type:", ""), true);
      } else if (group.startsWith("seen:")) {
        return (bug) => variantDescriptionMatch(bug, group.replace("seen:", ""));
      } else if (group.startsWith("!seen:")) {
        return (bug) => variantDescriptionMatch(bug, group.replace("!seen:", ""), true);
      } else if (group.startsWith("version:")) {
        return (bug) => variantBrowserVersionMatch(bug, group.replace("version:", ""));
      } else if (group.startsWith("!version:")) {
        return (bug) => variantBrowserVersionMatch(bug, group.replace("!version:", ""), true);
      } else {
        // Default case - search the style string
        return (bug) => styleContains(bug, group);
      }
    })

  return bugs.filter(bug => filters.every(f => f(bug)));
}