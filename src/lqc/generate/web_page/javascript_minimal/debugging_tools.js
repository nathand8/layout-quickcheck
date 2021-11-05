
// Helper function to output dimensions
// Output to be consumed by layout_comparer.py : compare_layout()
//
// Output Format: {
//   x: 10,
//   y: 10,
//   width: 1200,
//   height: 900,
//   children: [{...}, ...]
// }
function outputElementDimensions() {

  const recurse = (element) => {
    const { x, y, width, height } = element.getBoundingClientRect();
    const values = { x, y, width, height };
    values.children = Array.from(element.children).map((child) =>
      recurse(child)
    );
    return values;
  };

  return recurse(document.body);
}


// This function will take two dictionaires of dimensions and compare them
// Looks for dimensions that are NOT equal
function compareDimensions(dimensionsAfterModify, dimensionsAfterReload) {

  differences = []

  // Check that the two dictionaries have the same elements
  r_elem_dims = dimensionsAfterReload
  m_elem_dims = dimensionsAfterModify
  r_elems = Object.keys(dimensionsAfterReload)
  m_elems = Object.keys(dimensionsAfterModify)

  // Compare each set of dimensions for elements in both M and R
  shared_elems = r_elems.filter(el => m_elems.includes(el))

  if (shared_elems.length !== r_elems.length || shared_elems.length !== m_elems.length) {
    console.error("The two sets of dimensions don't have the same elements. (This should never happen) Dimensions after modification:", dimensionsAfterModify, " Dimensions after reload:", dimensionsAfterReload)
  }

  shared_elems.forEach(el => {
    m_el_dims = m_elem_dims[el]['dimensions']
    r_el_dims = r_elem_dims[el]['dimensions']
    differing_dims = []
    bounding_rect_attrs = ['x', 'y', 'left', 'right', 'top', 'bottom', 'height', 'width']
    for (attr of bounding_rect_attrs) {
      if (m_el_dims[attr] !== r_el_dims[attr]) {
        differing_dims.push(attr)
      }
    }

    if (differing_dims.length > 0) {
      post_modify_dims = Object.fromEntries(differing_dims.map( attr => [attr, m_el_dims[attr]] ));
      post_reload_dims = Object.fromEntries(differing_dims.map( attr => [attr, r_el_dims[attr]] ));
      console.log("Conflicting dimensions for element", el);
      console.log("    Dimensions after reload: ", JSON.stringify(post_reload_dims));
      console.log("    Dimensions after modify: ", JSON.stringify(post_modify_dims));
      differences.push({
        id: m_elem_dims[el]['id'],
        tag: m_elem_dims[el]['tag'],
        id_tag: el,
        differing_dims: differing_dims,
        post_modify_dims: post_modify_dims,
        post_reload_dims: post_reload_dims
      })
    }
  })

  // Return structure
  // [{
  //   id: one
  //   tag: div
  //   id_tag: one<div>
  //   differing_dims: ['x', 'left'],
  //   post_modify_dims: {x: 100, left: 10}
  //   post_reload_dims: {x: 120, left: 15}
  // }, ...]
  return differences
}

// Get all element dimensions on the page
// Output to be consumed by compareDimensions()
//
// Output format: {
//    'id<tag>': {BoundingClientRect},
//    'id<tag>': {BoundingClientRect},
//    ...
// }
const outputDimensions = () => {
  var dimensions = {}

  Array.from(document.getElementsByTagName('*')).forEach((element) => {
    var elementId = element.id;
    var tagName = element.tagName.toLowerCase();
    var elUniqueId = (elementId || "UnknownID") + "<" + tagName + ">";
    var boundingRect = element.getBoundingClientRect();
    dimensions[elUniqueId] = {
      'id': elementId,
      'tag': tagName,
      'dimensions': boundingRect,
    }
  });

  return dimensions
} 

// Reload all of the elements/styles on the page
function reload() {
}

//
// Run this function to see the differences between modifying styles vs loading them fresh
//
function checkForBug() {

  // console.log('Dimensions before application');
  // dimensionsBeforeApplication = outputDimensions();

  makeStyleChanges()

  dimensionsAfterApplication = outputDimensions();
  console.log('Dimensions after application', dimensionsAfterApplication);

  document.documentElement.innerHTML = document.documentElement.innerHTML;

  dimensionsAfterFreshLoad = outputDimensions();
  console.log('Dimensions after fresh load', dimensionsAfterFreshLoad);

  return compareDimensions(dimensionsAfterApplication, dimensionsAfterFreshLoad);
}

// https://css-tricks.com/snippets/javascript/get-url-variables/
function getQueryVariable(variable)
{
  var query = window.location.search.substring(1);
  var vars = query.split("&");
  for (var i=0;i<vars.length;i++) {
    var pair = vars[i].split("=");
    if(pair[0] == variable){return pair[1];}
  }
  return(false);
}
