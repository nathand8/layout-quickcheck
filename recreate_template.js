// This function will take two dictionaires of dimensions and compare them
// Looks for dimensions that are NOT equal
function compareDimensions(dimensionsAfterModify, dimensionsAfterReload) {

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
    m_el_dims = m_elem_dims[el]
    r_el_dims = r_elem_dims[el]
    conflicting_attrs = []
    bounding_rect_attrs = ['x', 'y', 'left', 'right', 'top', 'bottom', 'height', 'width']
    for (attr of bounding_rect_attrs) {
      if (m_el_dims[attr] !== r_el_dims[attr]) {
        conflicting_attrs.push(attr)
      }
    }

    if (conflicting_attrs.length > 0) {
      console.log("Conflicting dimensions for element", el);
      console.log("    Dimensions after reload: ", conflicting_attrs.map(attr => attr + ": " + String(r_el_dims[attr])).join(', '));
      console.log("    Dimensions after modify: ", conflicting_attrs.map(attr => attr + ": " + String(m_el_dims[attr])).join(', '));
    }
  })

}

// Get all element dimensions on the page
// Returns object in this format: {
//    'id<tag>': {BoundingClientRect},
//    'id<tag>': {BoundingClientRect},
//    ...
// }
const outputDimensions = () => {
  dimensions = {}

  Array.from(document.getElementsByTagName('*')).forEach((element) => {
    elUniqueId = (element.id || "UnknownID") + "<" + element.tagName.toLowerCase() + ">"
    boundingRect = element.getBoundingClientRect();
    dimensions[elUniqueId] = boundingRect
  });

  return dimensions
} 

// Make the style changes to the page
function makeStyleChanges() {
  const styleLog = __MODIFIED_STYLE_STRING__;

  Object.entries(styleLog).forEach(([id, styles]) => {
    const element = document.getElementById(id);
    if (element) {
      Object.entries(styles).forEach(([styleName, styleValue]) => {
        element.style[styleName] = styleValue;
      });
    }
  });
}

// Reload all of the elements/styles on the page
function reload() {
  document.documentElement.innerHTML = document.documentElement.innerHTML;
}

//
// Run this function to see the differences between modifying styles vs loading them fresh
//
function recreateTheProblem() {

  // console.log('Dimensions before application');
  // dimensionsBeforeApplication = outputDimensions();

  makeStyleChanges()

  dimensionsAfterApplication = outputDimensions();
  console.log('Dimensions after application', dimensionsAfterApplication);

  reload()

  dimensionsAfterFreshLoad = outputDimensions();
  console.log('Dimensions after fresh load', dimensionsAfterFreshLoad);

  compareDimensions(dimensionsAfterApplication, dimensionsAfterFreshLoad);
}