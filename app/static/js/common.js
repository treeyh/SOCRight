var Common = {
    alert: function (msg, gotoUrl) {
        if (msg != undefined &&  msg != '') {
            alert(msg);
            if (gotoUrl != undefined && gotoUrl != '') {
                window.location.href = gotoUrl;
            }
        }
    }
};