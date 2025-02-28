
// Record audio from the browser and send it to the server
document.addEventListener("DOMContentLoaded", function () {
    let rec, audioChunks = [];

    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => { handlerFunction(stream); });

    function handlerFunction(stream) {
        rec = new MediaRecorder(stream);
        rec.ondataavailable = e => {
            audioChunks.push(e.data);
            if (rec.state == "inactive") {
                let blob = new Blob(audioChunks, { type: 'audio/mpeg-3' });
                sendData(blob, activeButtonId);
            }
        };
    }

    let activeButtonId = "";  // Track which button is being used

    function sendData(data, buttonId) {
        var form = new FormData();
        form.append('file', data, 'data.mp3');
        form.append('title', 'data.mp3');
        form.append('button_id', buttonId);  // Send button ID

        if (buttonId === "recordButton") {
            form.append('language', document.getElementById('languageSelect').value);
        } else {
            form.append('language', document.getElementById('languageSelect2').value);
        }

        $.ajax({
            type: 'POST',
            url: '/mic-input',
            data: form,
            cache: false,
            processData: false,
            contentType: false
        }).done(function (data) {
            console.log(`Response from Flask for ${buttonId}:`, data);
            if (buttonId === "recordButton") {
                document.getElementById('transcription').value = data;
            } else {
                document.getElementById('transcription2').value = data;
            }
        }).fail(function (xhr) {
            let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "";
            alert(errorMessage); // Show popup error message
            if (buttonId === "recordButton") {
                document.getElementById('transcription').value = errorMessage;
            } else {
                document.getElementById('transcription2').value = errorMessage;
            }
        });
    }

    function toggleRecording(button) {
        let buttonId = button.id;  // Get button ID (recordButton or recordButton2)

        if (rec.state === "inactive") {
            console.log(`Recording started for ${buttonId}..`);
            button.classList.add('recording');
            audioChunks = [];
            rec.start();
            activeButtonId = buttonId;
        } else {
            console.log(`Recording stopped for ${buttonId}.`);
            button.classList.remove('recording');
            rec.stop();
        }
    }

    document.getElementById("recordButton").onclick = function () {
        toggleRecording(this);
    };

    document.getElementById("recordButton2").onclick = function () {
        toggleRecording(this);
    };
});

// Send the selected languages to the server
$(document).ready(function() {
    function sendLanguages() {
        let patientLan = $("#languageSelect").val();
        let workerLan = $("#languageSelect2").val();

        $.ajax({
            url: "/get-languages",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ patientLan: patientLan, workerLan: workerLan }),
            success: function(response) {
                console.log("Languages sent successfully:", response);
            },
            error: function(xhr, status, error) {
                console.error("Error sending languages:", error);
            }
        });
    }

    // Run once when the page loads (only if values exist)
    setTimeout(sendLanguages, 500);

    // Call function when the language is selected
    $("#languageSelect, #languageSelect2").change(sendLanguages);
});



// Play audio in browser
$(document).ready(function () {
    function playAudio(buttonId) {
        $.ajax({
            url: "/play-audio",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ button_id: buttonId }),
            xhrFields: {
                responseType: 'blob' // Expect binary data (MP3)
            },
            success: function (blob) {
                let audioURL = URL.createObjectURL(blob); // Convert to playable URL
                let audio = new Audio(audioURL);
                audio.play();
            },
            error: function (xhr) {
                let errorMessage = xhr.responseJSON && xhr.responseJSON.error ? xhr.responseJSON.error : "⚠️ Translation not available!";
                alert(errorMessage);
            }
        });
    }

    $("#playTTSButton").click(function () {
        playAudio("playTTSButton");
    });

    $("#playTTSButton2").click(function () {
        playAudio("playTTSButton2");
    });
});




// Populate the language dropdown and initialize Select2
$.getJSON('/static/languages.json', function(data) {
    
    
    //patient's language selection
    var languageSelect = $('#languageSelect');
    $.each(data.languages, function(key, entry) {
        languageSelect.append($('<option></option>')
            .attr('value', entry.code)
            .attr('data-english-name', entry.english_name)
            .text(entry.name));
    });
    languageSelect.select2({
        matcher: function(params, data) {
            if ($.trim(params.term) === '') {
                return data;
            }

            if (typeof data.text === 'undefined') {
                return null;
            }

            // Match the term with the English name
            var englishName = $(data.element).data('english-name');
            if (englishName && englishName.toLowerCase().indexOf(params.term.toLowerCase()) > -1) {
                return data;
            }

            return null;
        }
    });

    //health worker's language selection
    var languageSelect2 = $('#languageSelect2');
    $.each(data.languages, function(key, entry) {
        languageSelect2.append($('<option></option>')
            .attr('value', entry.code)
            .attr('data-english-name', entry.english_name)
            .text(entry.name));
    });


    languageSelect2.select2({
        matcher: function(params, data) {
            if ($.trim(params.term) === '') {
                return data;
            }

            if (typeof data.text === 'undefined') {
                return null;
            }

            // Match the term with the English name
            var englishName = $(data.element).data('english-name');
            if (englishName && englishName.toLowerCase().indexOf(params.term.toLowerCase()) > -1) {
                return data;
            }

            return null;
        }
    });
});


