var Common = {
    alert: function (msg, gotoUrl) {
        if (msg != undefined &&  msg != '') {
            alert(msg);
            if (undefined != gotoUrl && gotoUrl != '') {
                window.location.href = gotoUrl;
            }
        }
    },
    resetContent: function(){
        var h = $(window).height();
        var hh = $('.navbar').outerHeight(true);
        // var fh = $('#footer').outerHeight(true);
        var fh = 3;
        var height = h - hh - fh;
        if(height > 300){
            $('#wrap').height(height);
        }else{
            $('#wrap').height(300);
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