function filter(button){
    var filterDict = {
        "posfilter" : {
            off:".neg, .neu",
            on:".pos",
            inactive:"#negfilter, #neufilter, #allfilter"
        },
        "negfilter" : {
            off:".pos, .neu",
            on:".neg",
            inactive:"#posfilter, #neufilter, #allfilter"
        },
        "neufilter" : {
            off:".neg, .pos",
            on:".neu",
            inactive:"#negfilter, #posfilter, #allfilter"
        },
        "allfilter" : {
            off:"",
            on:".pos, .neg, .neu",
            inactive:"#negfilter, #neufilter, #posfilter"
        }
    }
    $(filterDict[button].off).hide();
    $(filterDict[button].on).show();
    $("#"+button).addClass("active");
    $(filterDict[button].inactive).removeClass("active");
}

$(document).ready(function() {
    $("#posfilter, #negfilter, #neufilter, #allfilter").on("click", function(){
        filter(this.id);
    });
});