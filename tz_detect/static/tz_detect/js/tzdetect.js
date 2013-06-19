(function(){
    var createXMLHttp = function() {
        var xmlHttp = null;
        // Use XMLHttpRequest where available
        if (typeof(XMLHttpRequest) !== undefined) {
            xmlHttp = new XMLHttpRequest();
            return xmlHttp;
        // IE
        } else if (window.ActiveXObject) {
            var ieXMLHttpVersions = ['MSXML2.XMLHttp.5.0', 'MSXML2.XMLHttp.4.0', 'MSXML2.XMLHttp.3.0', 'MSXML2.XMLHttp', 'Microsoft.XMLHttp'];
            for (var i = 0; i < ieXMLHttpVersions.length; i++) {
                    try {
                        xmlHttp = new ActiveXObject(ieXMLHttpVersions[i]);
                        return xmlHttp;
                    } catch (e) {}
            }
        }
    };

    var xmlHttp = createXMLHttp();
    if(xmlHttp) {
        xmlHttp.open('post', window.tz_set_endpoint, true);
        xmlHttp.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        xmlHttp.setRequestHeader('X-CSRFToken', window.csrf_token);
        xmlHttp.send("offset=" + (new Date()).getTimezoneOffset());
    }

}());