/** Functions for button */

if (typeof window.SwitchButton === 'undefined') {
    window.SwitchButton = function() {};

    window.SwitchButton.getSwitchFunctionName = function ($btn) {
        var id = $btn.attr('id');
        return id.replace(/-/g, '_') + '_SWITCH';
    };

    window.SwitchButton.changeSwitchDisplay = function ($btn, value, colors, icons, alts) {
        if (value) {
            $btn.removeClass('text-' + colors[0]).addClass('text-' + colors[1]);
            $btn.find('span.sr-only').html(alts[1]);
            $btn.find('.fa-' + icons[0]).removeClass('.fa-' + icons[0]).addClass('fa-' + icons[1]);
        } else {
            $btn.removeClass('text-' + colors[1]).addClass('text-' + colors[0]);
            $btn.find('span.sr-only').html(alts[0]);
            $btn.find('.fa-' + icons[1]).removeClass('.fa-' + icons[1]).addClass('fa-' + icons[0]);
        }
    };
}
