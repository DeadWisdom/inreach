function collapsingSection(index, e) {
    var self = $(e);
    var header = self.prev('h1').addClass('collapser');
    self.hide();
    header.click(function() {
        self.toggle();
        header.toggleClass('expanding');
    });
}

$(function() {
    $('section.collapse').each(collapsingSection);
})