var justShown = false;

function toggleDropdown(id) {
  document.getElementById('card-dropdown-' + id).classList.toggle("show");
  justShown = true;
}

document.addEventListener('long-press', function(e) {
    if (e.target.classList.contains('longpress')) {
        id = e.target.getAttribute('id');
        toggleDropdown(id);
    }
});

window.addEventListener('click', function(e) {
    if (justShown) {
        justShown = false;
    } else {
        var popup = document.querySelector('.show');
        if (popup && e.target !== popup && !popup.contains(e.target)) {
            popup.classList.remove('show');
        }
    }
});

!function(t,e){"use strict";function n(){this.dispatchEvent(new CustomEvent("long-press",{bubbles:!0,cancelable:!0})),clearTimeout(o),console&&console.log&&console.log("long-press fired on "+this.outerHTML)}var o=null,u="ontouchstart"in t||navigator.MaxTouchPoints>0||navigator.msMaxTouchPoints>0,s=u?"touchstart":"mousedown",i=u?"touchcancel":"mouseout",a=u?"touchend":"mouseup",c=u?"touchmove":"mousemove";"initCustomEvent"in e.createEvent("CustomEvent")&&(t.CustomEvent=function(t,n){n=n||{bubbles:!1,cancelable:!1,detail:void 0};var o=e.createEvent("CustomEvent");return o.initCustomEvent(t,n.bubbles,n.cancelable,n.detail),o},t.CustomEvent.prototype=t.Event.prototype),e.addEventListener(s,function(t){var e=t.target,u=parseInt(e.getAttribute("data-long-press-delay")||"1500",10);o=setTimeout(n.bind(e),u)}),e.addEventListener(a,function(t){clearTimeout(o)}),e.addEventListener(i,function(t){clearTimeout(o)}),e.addEventListener(c,function(t){clearTimeout(o)})}(this,document);