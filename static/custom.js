$(document).ready(function(){
     $("#posfilter").click(function(){
        $(".pos").show();
        $(".neg").hide();
        $(".neu").hide();
    });
    $("#negfilter").click(function(){
        $(".neg").show();
        $(".pos").hide();
        $(".neu").hide();
    });
    $("#neufilter").click(function(){
        $(".neu").show();
        $(".neg").hide();
        $(".pos").hide();
    });
    $("#allfilter").click(function(){
        $(".neu").show();
        $(".neg").show();
        $(".pos").show();
    });
});