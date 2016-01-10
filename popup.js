function getCurrentTabUrl(callback) {
  console.log('meow');
  var queryInfo = {
    active: true,
    currentWindow: true
  };
  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    callback(url);
  });
}

function submitMe() {
  var less = document.getElementById('less').value;
  var more = document.getElementById('more').value;
  getCurrentTabUrl(function(url) {
    chrome.tabs.create({ url: 'http://google.com' });
  });
}

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('submit').addEventListener('onsubmit', function(evt) {
    evt.preventDefault();
    submitMe();
  });
});
