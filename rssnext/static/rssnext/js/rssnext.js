function readCookie(n){return(n=new RegExp('(?:^|;\\s*)'+(''+n).replace(/[-[\]{}()*+?.,\\^$|#\s]/g,'\\$&')+'=([^;]*)').exec(document.cookie))&&n[1];}

function make_alert(message) {
    var alert = $('<div class="alert alert-danger alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + message + '</div>');
    $("#alert_messages").append(alert);
}