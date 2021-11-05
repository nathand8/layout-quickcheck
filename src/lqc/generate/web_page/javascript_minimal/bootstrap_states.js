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