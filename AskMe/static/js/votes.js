$('.js-votes').click(function(ev) {
    var $this = $(this),
        action = $this.data('action'),
        id = $this.data('id');
    $.ajax('/votes/', {
        method: 'POST',
        data: {
            action: action,
            id: id,
        },
    }).done(function(data) {
        like = data.question_like,
        $('#rating-' + id).text(data.rating);
    });
    console.log("Click! " + action + " " + id);
})
