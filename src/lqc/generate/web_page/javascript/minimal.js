function filterDimensions(obj, differing_dims) {{
  // Only show dimensions that were different after reload
  let ret = {{ }};
  differing_dims.forEach((dim) => {{
    ret[dim] = obj[dim];
  }});
  return ret;
}}

// Make the style changes to the page
function makeStyleChanges() {{
  {make_style_changes}
}}

function simpleRecreate() {{
  // Make the style changes
  makeStyleChanges();

  // Get the dimensions
  console.log("Dimensions after style changes, before reload");
  {get_dimensions}

  // Reload the elements
  document.documentElement.innerHTML = document.documentElement.innerHTML;

  // Get the dimensions again
  console.log("Dimensions after reload");
  {get_dimensions}
}}