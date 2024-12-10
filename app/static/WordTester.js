function checkWord(word) {
    console.log("the word testing is", word);
    $.ajax({
        url: '/word_check',
        type: 'POST',
        data: JSON.stringify({ word: word}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response){
            console.log("WOOOO");
            console.log("the word is", response.valid);
            if (response.valid == "true") {
                newGuess = document.createElement("li");
                newGuess.innerHTML = word;
                guesses.appendChild(newGuess);
            }
        },
        error: function(){
            console.log("error checking word validity");
        }
    });
}

$(document).ready(function() {
    var csrf_token = $('meta[name=csrf-token]').attr('content');
  $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    answer = document.getElementById("answer");
    guesses = document.getElementById("words_found")
    
})