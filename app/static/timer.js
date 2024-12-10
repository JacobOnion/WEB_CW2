$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    timer = document.getElementById("timer");
    finish = document.getElementById("finish");
    guessesList = document.getElementById("words_found")
    id = document.getElementById("score");
    if (id != null)
        id = id.innerHTML;

    if (timer != null) {
        var time = 60;
        console.log("tick");
        var countdown = setInterval(function() {
            timer.innerHTML = time-1;
            time-=1;
            if (time <= 0) {
                clearInterval(countdown);
                finish.style.display = "block";
                finish.style.visibility = "visible";
                guessesList.style.visibility = "none";

                var score = 0;
                var answerList = document.getElementById("words_found");
                var guesses = $(answerList).children();
                for (const word of guesses) {
                    console.log("WORD CHECK IS", word.innerHTML);
                    score += word.innerHTML.length;
                }
                document.getElementById("score").innerHTML = score;

                $.ajax({
                    url: '/submit_score',
                    type: 'POST',
                    data: JSON.stringify({ score: score, puzzleId: id}),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function(response){
                        console.log("score submitted");
                    },
                    error: function(){
                        console.log("failed to submit score");
                    }
                });
            }
        }, 1000)
    }
})