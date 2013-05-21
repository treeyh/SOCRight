var Common = {
    alert: function (msg, gotoUrl, goLevel) {
        if (msg != undefined &&  msg != '') {
            alert(msg);
            if (undefined != gotoUrl && gotoUrl != '') {
                window.location.href = gotoUrl;
            }
            if (undefined != goLevel && goLevel != '' && goLevel < 0){
            	window.history.go(goLevel);
            }
        }
    }
};