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
    backPage:function(){
        var url = $('#refUrl').val();
        if(undefined == url || '' == url){
            return;
        }
        window.location.href = url;
    },
    goToPage: function(url, pageTotal){
        var page = $('#btGoToPage').val();
        var p = parseInt(page);
        if(p <= 0 || p > pageTotal){
            Common.alert('填入数量不符合要求.');
            return;
        }
        url = url + p;
        if($('#refUrl').length > 0 && url.indexOf('refUrl=') < 0){
            var aback = $('#refUrl')[0].href;
            url = "&refUrl="+enencodeURIComponent(aback);
        }

        window.location.href = url;
    }
};

