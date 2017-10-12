/** Functions for button */
const DEBUG_SWITCH = true;


if (typeof window.switchButtons === 'undefined') {

    // Creates a namespace where lives the switchButtons
    window.switchButtons = function () {
    };

    window.switchButtons.getSwitchFunctionName = function ($btn) {
        var id = $btn.attr('id');
        return id.replace(/-/g, '_').toUpperCase() + '_SWITCH';
    };

    window.switchButtons.changeSwitchDisplay = function ($btn, value, colors, icons, alts) {
        // Sets the data-value attribute to the new value
        $btn.data('value', value);
        if (DEBUG_SWITCH) {
            console.debug('switchButtons.changeSwitchDisplay() icons = "{0}"'.format(icons.join(',')));
            console.debug('switchButtons.changeSwitchDisplay() colors = "{0}"'.format(colors.join(',')));
            console.debug('switchButtons.changeSwitchDisplay() alts = "{0}"'.format(alts.join(',')));
        }

        // Changes the button display
        if (value) {
            // Change color
            $btn.find('.switch-icon').removeClass('text-' + colors[0]).addClass('text-' + colors[1])
            // Change icon
                .find('.fa').removeClass('fa-' + icons[0]).addClass('fa-' + icons[1])
            // Change title
                .attr('title', alts[1]);
        } else {
            // Change color
            $btn.find('.switch-icon').removeClass('text-' + colors[1]).addClass('text-' + colors[0])
            // Change icon
                .find('.fa').removeClass('fa-' + icons[1]).addClass('fa-' + icons[0])
            // Change title
                .attr('title', alts[0]);
        }
    };
}
