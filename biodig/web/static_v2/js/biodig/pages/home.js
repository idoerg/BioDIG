require.config({
    shim: {
        jquery: {
            init: function() {
                return $;
            }
        },
        bootstrap: ['jquery'],
        jquery_ui: ['jquery'],
        underscore : {
            exports : '_'
        }
    },
    paths: {
        jquery: 'lib/jquery-1.11.0.min',
        underscore: 'lib/underscore.min',
        bootstrap: 'lib/bootstrap.min',
        settings: 'lib/settings',
        jquery_ui: 'lib/jquery-ui-1.8.21.min',
        text: 'lib/require-text'
    }
});

var deps = [
    'jquery', 'underscore', 'settings', 'biodig/ui/ZoomableUI',
    'text!biodig/tmpl/helpbox.html', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, ZoomableUI, HelpBox) {

    $(function() {
        $( "#selectable" ).selectable();
    });

    $('#search_selected button').bind('click', function() {
        var selected_id = $('.ui-selected').map(function() {
            return this.id;
        }).get().join(',');

        if (selected_id != "") {
              var form = document.createElement("form");
            form.setAttribute("method", "get");
            form.setAttribute("action", settings.SITE_URL + "search/");
            hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", "organismId");
            hiddenField.setAttribute("value", selected_id);
            form.appendChild(hiddenField);
            form.appendChild($('#searchGenomes').clone()[0]);
            form.appendChild($('#searchImages').clone()[0]);
            document.body.appendChild(form);
            form.submit();
        }
    });

    $('#mycoplasma_selector_menu ol li').dblclick(function() {
        var form = document.createElement("form");
        form.setAttribute("method", "get");
        form.setAttribute("action", settings.SITE_URL + "search/");
        hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", "organismId");
        hiddenField.setAttribute("value", $(this).attr('id'));
        form.appendChild(hiddenField);
        form.appendChild($('#searchGenomes').clone()[0]);
        form.appendChild($('#searchImages').clone()[0]);
        document.body.appendChild(form);
        form.submit();
    });

    ZoomableUI.create('#phylogenetic_tree', {
        height: 800,
        width: 660,
        actualImageSrc: settings.STATIC_URL + 'images/mycoplasma_tree_hiRes.png'
    });

    var helpDialog = $(_.template(HelpBox)(settings));

    $('#helpButton').click(function() {
        var box = $(helpDialog.attr('id'));
        if (box.length > 0) {
            box.modal('show');
        }
        else {
            helpDialog.appendTo($('body')).modal();
        }
    });
});
