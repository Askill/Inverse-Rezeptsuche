function getJSON(url, callback, fallback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function () {
        var status = xhr.status;
        if (status < 400) {
            callback(null, xhr.response);
        } else {
            fallback();
        }
    };
    xhr.send();
};
