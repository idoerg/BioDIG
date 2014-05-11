function PageBlock() {
    this.block = $('<div />');
    this.block.addClass('page-block');    
    $('body').append(this.block);
};

PageBlock.prototype.show = function() {
    this.block.height($(window).height());
    this.block.width($(window).width());
    
    var block = this.block;
    
    $(window).resize(function() {
        block.height($(this).height());
        block.width($(this).width());
    });
    
    this.block.show();
};

PageBlock.prototype.hide = function() {
    $(window).off('resize');
    this.block.hide();
};