function typeMatch(bug, s) {
  return bug.bug_type.toLowerCase().includes(s.toLowerCase());
}

function variantDescriptionMatch(bug, s) {
  return bug.variants["Test Variant Details"]
          .filter(variant => variant.bug_detected)
          .map(variant => variant.description.replace(/\s+/g, '')) // remove all whitespace
          .join(', ')
          .toLowerCase()
          .includes(s.toLowerCase());
}

function styleContains(bug, s) {
  return bug.styles_used_string.toLowerCase().includes(s.toLowerCase());
}

function variantBrowserVersionMatch(bug, s) {
  return bug.variants["Test Variant Details"]
          .filter(variant => variant.bug_detected)
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
      } else if (group.startsWith("seen:")) {
        return (bug) => variantDescriptionMatch(bug, group.replace("seen:", ""));
      } else if (group.startsWith("version:")) {
        return (bug) => variantBrowserVersionMatch(bug, group.replace("version:", ""));
      } else {
        // Default case - search the style string
        return (bug) => styleContains(bug, group);
      }
    })

  return bugs.filter(bug => filters.every(f => f(bug)));
}