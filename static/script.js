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
                sendData(blob, activeMic);
            }
        };
    }

    let activeMic = 1;  // Track which mic is being used

    function sendData(data, micId) {
        var form = new FormData();
        form.append('file', data, 'data.mp3');
        form.append('title', 'data.mp3');

        if (micId === 1) {
            form.append('language', document.getElementById('languageSelect').value);
        } else {
            form.append('language', document.getElementById('languageSelect2').value);
        }

        $.ajax({
            type: 'POST',
            url: '/save-record',
            data: form,
            cache: false,
            processData: false,
            contentType: false
        }).done(function (data) {
            console.log(data);
            if (micId === 1) {
                document.getElementById('transcription').value = data;
            } else {
                document.getElementById('transcription2').value = data;
            }
        });
    }

    function toggleRecording(button, micId) {
        if (rec.state === "inactive") {
            console.log(`Recording started for mic ${micId}..`);
            button.classList.add('recording');
            audioChunks = [];
            rec.start();
            activeMic = micId;
        } else {
            console.log(`Recording stopped for mic ${micId}.`);
            button.classList.remove('recording');
            rec.stop();
        }
    }

    document.getElementById("recordButton").onclick = function () {
        toggleRecording(this, 1);
    };

    document.getElementById("recordButton2").onclick = function () {
        toggleRecording(this, 2);
    };
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


