// Get variable by key name from url query string
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

// Query strings can load page with particular state
// state=initial - page before any changes are made (default)
// state=dirty - page after changes
// state=reloaded - page after changes and reload
// delay=1000 - delay the state change until 1000ms (optional, default is 500 ms)
(function() {
    var state = (getQueryVariable("state") || "initial").toLowerCase();
    var delay = parseInt(getQueryVariable("delay")) || 1000;
    if (state == "dirty") {
    setTimeout(function() {
        makeStyleChanges();
    }, delay)
    } else if (state == "reloaded") {
    setTimeout(function() {
        makeStyleChanges();
        setTimeout(function() {
        reload();
        }, 100);
    }, delay);
    }
})();