function simpleRecreate() {{
  // Make the style changes
  {make_style_changes}
  // Get the dimensions
  console.log("Dimensions after style changes, before reload");
  {get_dimensions}
  // Reload the elements
  document.documentElement.innerHTML = document.documentElement.innerHTML;

  // Get the dimensions again
  console.log("Dimensions after reload");
  {get_dimensions}
}}