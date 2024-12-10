$(document).ready(function() {
    items = document.getElementsByClassName("letter_box");
    var currentLetter;
    var nextPos;
    letterRow = document.getElementById("drop_boxes");
    answer = document.getElementById("answer");
    if (answer != null) {
        nextPos = $(answer).offset().left - $(answer).width() - 20;
    }
    //answerLine = document.getElementById("answer_line");
    //answerPos = answerLine.getBoundingClientRect();
    //answer.style.top = answerPos.top + "px";
    //answer.style.left = answerPos.left + "px";
    //$(answer).css({top: answerPos.top, left: answerPos.left});
    //console.log(answer.style.top);
    //console.log(answerLine.style.top);
    SetLetterRow();

    for (item of items) {
        //console.log(item.getAttribute("data-letter"));
        console.log(item.id);

        item.addEventListener("dragstart", (event) => {
            console.log("DRAGGIN");
            currentLetter = event.target.id;
            //console.log(currentLetter);
            //event.target.style.display = "none";
            //event.target.style.visibility = "none";
            /*if ($(event.target).parent().attr("id") == "answer") {
                $(answer).children().each(function() {
                    console.log("BEEEWAANS");
                    var child = $(this);
                    console.log($(child).offset().left);
                    if ($(child).offset().left > $(letter).offset().left) {
                        console.log("shifting");
                        $(child).css("left", (parseFloat($(child).css("left"))) - 60 + "px");
                    }
                })
            }*/
        })

        item.addEventListener("ondrop", (event) => {
        console.log("returning");
        item.style.position = "relative";
        event.preventDefault();
        letterRow.appendChild(item);
        })

        item.addEventListener("dragend", (event) => {
            console.log("DROPPED");
            //event.target.style.display = "block";
            //event.target.style.visibility = "visible";
        })
    }

    function SetLetterRow() {
        var childrenNum = $(letterRow).children().length;
        var childIndex = 0;
        $(letterRow).children().each(function() {
            $(this).css("position", "absolute");
            var childPos = (100 / childrenNum-1) * childIndex;
            $(this).css("left", childPos + 10 + "%");
            childIndex+=1;
        })
    }

    function getWord() {
        var word = "";
        $(answer).children().each(function () {
            word += this.getAttribute("data-letter");
        })
        checkWord(word);
    }

    if (answer != null) {
        answer.addEventListener("dragover", (event) => {
            event.preventDefault();
        })

        letterRow.addEventListener("dragover", (event) => {
            event.preventDefault();
        })

        letterRow.addEventListener("drop", (event) => {
            console.log("retreating");
            event.preventDefault();
            letter = document.getElementById(currentLetter);
            if ($(letterRow).children("#"+currentLetter).length > 0) {
                console.log("already in row");
            }
            else {
                console.log("not in row");
                $(answer).children().each(function shift() {
                    var child = $(this);
                    console.log($(child).offset().left);
                    if ($(child).offset().left > $(letter).offset().left) {
                        console.log("shifting");
                        $(child).css("left", (parseFloat($(child).css("left"))) - 60 + "px");
                    }
                })
                nextPos -= 60;
            }
            letterRow.appendChild(letter);
            SetLetterRow();
            getWord();
        })

        answer.addEventListener("drop", (event) => {
            console.log("appending");
            event.preventDefault();
            letter = document.getElementById(currentLetter);
            if ($(event.target).children("#"+currentLetter).length > 0) {
                console.log("repeated");
                $(answer).children().each(function shift() {
                    var child = $(this);
                    console.log($(child).offset().left);
                    if ($(child).offset().left > $(letter).offset().left) {
                        console.log("shifting");
                        $(child).css("left", (parseFloat($(child).css("left"))) - 60 + "px");
                    }
                })
                nextPos -= 60;
            }
            event.target.appendChild(letter);
            letter.style.position = "absolute";
            letter.style.left = nextPos + "px";
            nextPos += 60;
            letter.style.top = $(answer).offset.top + "px";
            getWord();
        })
    }
});