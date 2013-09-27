var Common = {
    alert: function (msg, gotoUrl) {
        if (msg != undefined &&  msg != '') {
            alert(msg);
            if (undefined != gotoUrl && gotoUrl != '') {
                window.location.href = gotoUrl;
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
        url = url + p;
        if($('#aback').length > 0 && url.indexOf('refUrl=') < 0){
            var aback = $('#aback')[0].href;
            url = "&refUrl="+enencodeURIComponent(aback);
        }

        window.location.href = url;
    }
};