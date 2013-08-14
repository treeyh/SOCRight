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
    },

    goToPage: function(url, pageTotal){
        var page = $('#btGoToPage').val();
        var p = parseInt(page);
        if(p <= 0 || p > pageTotal){
            Common.alert('填入数量不符合要求.');
            return;
        }
        window.location.href = url+p;
    }
};