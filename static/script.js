// This script is used to record audio and send it to the server.

navigator
    .mediaDevices
    .getUserMedia({audio: true})
    .then(stream => { handlerFunction(stream) });

function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = e => {
        audioChunks.push(e.data);
        if (rec.state == "inactive") {
            let blob = new Blob(audioChunks, {type: 'audio/mpeg-3'});
            sendData(blob);
        }
    }
}

function sendData(data) {
    var form = new FormData();
    form.append('file', data, 'data.mp3');
    form.append('title', 'data.mp3');
    form.append('language', document.getElementById('languageSelect').value);
    //Chrome inspector shows that the post data includes a file and a title.
    $.ajax({
        type: 'POST',
        url: '/save-record',
        data: form,
        cache: false,
        processData: false,
        contentType: false
    }).done(function(data) {
        console.log(data);
        document.getElementById('transcription').value = data;
    });
}

recordButton.onclick = e => {
    if (rec.state == "inactive") {
        console.log('Recording started..');
        // recordButton.textContent = 'Stop recording';
        recordButton.classList.add('recording');
        audioChunks = [];
        rec.start();
    } else {
        console.log("Recording stopped.");
        // recordButton.textContent = 'Start recording';
        recordButton.classList.remove('recording');
        rec.stop();
    }
};

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


