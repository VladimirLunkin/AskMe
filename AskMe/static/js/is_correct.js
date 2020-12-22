$('.js-correct').click(function(ev) {
    let $this = $(this),
        id = $this.data('id');
    $.ajax('/correct/', {
        method: 'POST',
        data: {
            id: id,
        },
    }).done(function(data) {
        $('#correct-' + id).prop('checked', data.action);
    });
    console.log("Correct is " + id);
})
