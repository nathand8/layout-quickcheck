
export function applySearch(searchStr, bugs) {
  let groups = searchStr.split(/[ ,]+/); // Split by whitespace
  let filters = groups
    .filter(group => group.length > 0)
    .map((group) => {
      if (group.startsWith("type:")) {
        return (bug) => (bug.bug_type.toLowerCase().includes(group.replace("type:", "").toLowerCase()));
      } else if (group.startsWith("seen:")) {
        return (bug) => (bug.variants["Test Variant Details"].filter(variant => variant.bug_detected).map(variant => variant.description).join(', ').toLowerCase().includes(group.replace("seen:", "").toLowerCase()))
      } else {
        return (bug) => (bug.styles_used_string.includes(group));
      }
    })
  return bugs.filter(bug => filters.every(filter => filter(bug)));
}