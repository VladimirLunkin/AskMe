$('.js-votes').click(function(ev) {
    let $this = $(this),
        type = $this.data('type'),
        id = $this.data('id'),
        action = $this.data('action');
    $.ajax('/votes/', {
        method: 'POST',
        data: {
            type: type,
            id: id,
            action: action,
        },
    }).done(function(data) {
        like = data.question_like,
        $('#rating-' + id).text(data.rating);
    });
    console.log(type + " " + id + ": " + action);
})
