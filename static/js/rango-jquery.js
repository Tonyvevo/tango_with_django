$(document).ready(function(){
    $("#about-btn").click(function(event){
        alert("You clicked the button using JQuery!");
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo"
        $("#msg").html(msgstr)
    });
    $("#about-btn").addClass('btn btn-primary')
    $("p").hover( function(){
        $(this).css('color', 'red');
    },
    function(){
        $(this).css('color', 'blue');
	});
});
