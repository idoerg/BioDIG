var deps = [
    'jquery', 'underscore', 'biodig/ui/menu/Menu',
    'biodig/ui/menu/MenuSection', 'biodig/ui/menu/MenuItem', 'lib/settings'
];

define(deps, function($, _, Menu, MenuSection, MenuItem, settings) {

    var ImageMenuHelper = {
        createPublicMenu: function(toolbar) {
            var menu = Menu.create(toolbar);

            // create tools menu section
            var tools = menu.section('tools', 'Tools', 'img[' + settings.STATIC_URL +
                'images/tools.png]');
            tools.item('download', 'Download Image Data', 'ui-icon ui-icon-disk');
            tools.item('zoomIn', 'Zoom In', 'ui-icon ui-icon-zoomin');
            tools.item('zoomOut', 'Zoom Out', 'ui-icon ui-icon-zoomout');
            tools.item('toggleTags', 'Toggle All Tag Visibility', 'img[' + settings.STATIC_URL +
                'images/eye.png]');

            // create the tag groups menu section
            var tagGroups = menu.section('tagGroups', 'Tag Groups', 'img[' + settings.STATIC_URL +
                'tagGroupIcon.png]');
            tagGroups.item('changeVisibleGroups', 'Change Visible Tag Groups',
                'ui-icon ui-icon-pencil');

            return menu;
        },
        createRegisteredMenu: function(menu) {
            // finish the tag groups section
            var tagGroups = menu.section('tagGroups');
            tagGroups.item('add', 'Add New Tag Group', 'ui-icon ui-icon-plusthick');
            tagGroups.item('edit', 'Edit Tag Group', 'ui-icon ui-icon-pencil');
            tagGroups.item('delete', 'Delete Tag Group', 'ui-icon ui-icon-trash');

            // create organism menu section
            var organisms = menu.section('organisms', 'Organisms on Image', 'img[' +
                settings.STATIC_URL + 'organismIcon.png]');
            organisms.item('add', 'Add Organism', 'ui-icon ui-icon-plusthick');
            organisms.item('delete', 'Remove Organism', 'ui-icon ui-icon-trash');

            // create tag groups menu section
            var tags = menu.section('tags', 'Tags', 'img[' + settings.STATIC_URL +
                'images/tag.png]');
            tags.item('add', 'Add New Tag', 'ui-icon ui-icon-plusthick');
            tags.item('edit', 'Edit Tag', 'ui-icon ui-icon-pencil');
            tags.item('delete', 'Delete Tag', 'ui-icon ui-icon-trash');

            // create gene links menu section
            var geneLinks = menu.section('geneLinks', 'Gene Links', 'img[' + settings.STATIC_URL +
                'images/geneLinksIcon.png]');
            geneLinks.item('add', 'Add New Gene To Tag', 'ui-icon ui-icon-plusthick');
            geneLinks.item('delete', 'Delete Gene From Tag', 'ui-icon ui-icon-trash');
        }
    };

    return {
        create: function(toolbar, mode) {
            var menu = ImageMenuHelper.createPublicMenu(toolbar);
            if (mode == 'REGISTERED') {
                ImageMenuHelper.addRegisteredMenu(menu);
            }
            return menu;
        }
    };
});
