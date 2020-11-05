// minified file auto-min-1-base.html 
// minified modified file auto-min-1-base-modified.html 
// manual minified file auto-min-1.html 
// manual minified modified file auto-min-1-modified.html 

Object.entries(styleLog).forEach(([id, styles]) => {
  const element = document.getElementById(id);
  Object.entries(styles).forEach(([styleName, styleValue]) => {
    element.style[styleName] = styleValue;
  });
});

Object.entries(styleLog).forEach(([id, styles]) => {
  const element = window.frames[0].document.getElementById(id);
  if (element) {
    Object.entries(styles).forEach(([styleName, styleValue]) => {ƒ
      element.style[styleName] = styleValue;
    });
  }
});
const baseLog = {"0cf2393e56a1481f9faea8157c9faa6b": {"display": "inline"}}
const styleLog = {"0cf2393e56a1481f9faea8157c9faa6b": {"padding-left": "+651vw"}}
const stylesUsed = ["display", "padding-left"]
const stylesUsedString = "display,padding-left"
