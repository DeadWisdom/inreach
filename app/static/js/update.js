window.last_update_id = null;

function update() {
    $.ajax({
        url: '/poll/',
        data: {'since': window.last_update_id},
        success: updateSuccess,
        error: updateError
    })
}

function updateSuccess(status) {
    try {
        if (status) {
            $('#status').empty().append(status.status);
            var updates = status.updates;
            if (updates.length > 0)
                last_update_id = updates[0].id;
            
            for(var i = 0; i < updates.length; i++) {
                var update = updates[i];
                if (update.type == 'updated') {
                    jQuery.map(updates[i].data, addMessage);
                }
            }
        }
    } catch(e) {}
    
    setTimeout(update, 5000);
}

function updateError() {
    setTimeout(update, 5000);
}

function addMessage(m, i) {
    var item = $('#message-template').children().clone();
    for(var k in m) {
        var value = m[k];
        item.find('.' + k).empty().append(value);
    }
    $('#message-list').prepend(item).find('em').remove();
    item.hide().fadeIn(500 + i * 20);
}

$(function() {
    setTimeout(update, 5000);
})