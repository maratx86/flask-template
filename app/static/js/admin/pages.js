$(function () {
    $('#preview-button').on('click', function () {
        $('<div class="preview-holder"><iframe id="preview-container" class="preview-container"></iframe><div class="preview-actions"><button onclick="$(\'.preview-holder\').remove();">Close</button></div></div>')
            .appendTo('body');
        $.ajax({
            url: "/page/",
            method: 'POST',
            contentType: "application/json",
            data: JSON.stringify({
                content: $('textarea#content')[0].value,
                title: $('#title')[0].value,
            }),
            dataType: 'html',
            success: function (data) {
                console.dir(data);
                let iframe = $('#preview-container')[0];
                iframe = iframe.contentWindow || ( iframe.contentDocument.document || iframe.contentDocument);
                iframe.document.open();
                iframe.document.write(data);
                iframe.document.close();
                },
        });
    });
})