require.config({
    shim: {
        jquery: {
            init: function() {
                return $;
            }
        },
        bootstrap: ['jquery'],
        jquery_ui: ['jquery'],
        colorpicker: ['jquery'],
        underscore : {
            exports : '_'
        },
        kinetic: {
            init: function() {
                return Kinetic;
            }
        }
    },
    paths: {
        jquery: 'lib/jquery-1.11.0.min',
        underscore: 'lib/underscore.min',
        bootstrap: 'lib/bootstrap.min',
        settings: 'lib/settings',
        jquery_ui: 'lib/jquery-ui-1.10.4.min',
        text: 'lib/require-text',
        kinetic: 'lib/kinetic-v5.1.0.min',
        colorpicker: 'lib/colorpicker/colorpicker'
    }
});

var deps = [
    'jquery', 'underscore', 'settings', 'biodig/ui/taggable/Taggable', 'biodig/ui/users/Login',
    'text!biodig/tmpl/helpbox/imageviewer.html', 'bootstrap', 'jquery_ui'
];

require(deps, function($, _, settings, Taggable, Login, HelpBox) {
    // Usage:
//
// 1. Put this in the file that gets first loaded by RequireJS
// 2. Once the page has loaded, type window.rtree.map() in the console
//    This will map all dependencies in the window.rtree.tree object
// 3. To generate UML call window.rtree.toUml(). The output can be used
//    here: http://yuml.me/diagram/scruffy/class/draw
requirejs.onResourceLoad = function (context, map, depMaps) {
  if (!window.rtree) {
    window.rtree = {};
    window.rtree.tree = {};
	window.rtree.map = function() {
	  var dep, key, rt, val, _i, _len, _ref;
	  rt = rtree.tree;
	  for (key in rt) {
		val = rt[key];
		if (rt.hasOwnProperty(key)) {
		  _ref = val.deps;
		  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
		    dep = _ref[_i];
		    val.map[dep] = rt[dep];
		  }
		}
	  }
	};
	window.rtree.toUml = function() {
	  var dep, key, rt, uml, val, _i, _len, _ref;
	  rt = rtree.tree;
	  uml = [];
	  for (key in rt) {
		val = rt[key];
		if (rt.hasOwnProperty(key)) {
		  _ref = val.deps;
		  for (_i = 0, _len = _ref.length; _i < _len; _i++) {
		    dep = _ref[_i];
		    uml.push("[" + key + "]->[" + dep + "]");
		  }
		}
	  }
	  return uml.join("\n");
	};

  }
  r = window.rtree.tree;
  o = {deps: [], map: {}};
  if (!r[map.name]) {
    r[map.name] = o;
  }
  if (map.parentMap && map.parentMap.name) {
    if (!r[map.parentMap.name]) {
      r[map.parentMap.name] = o;
    }
    if (map.parentMap.name !== map.name) {
      r[map.parentMap.name].deps.push(map.name);
    }
  }
};

    // setup the help dialog box for this page
    var helpDialog = $(_.template(HelpBox).call(settings));

    $('#helpButton').click(function() {
        var box = $(helpDialog.attr('id'));
        if (box.length > 0) {
            box.modal('show');
        }
        else {
            helpDialog.appendTo($('body')).modal();
        }
    });

    // setup login and logout forms
    var login = Login.create();
    $('.login > a').on('click', function() {
        login.show();
    });

    $('.logout > a').on('click', function() {
        var form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", settings.SITE_URL + "logout/");
        document.body.appendChild(form);
        form.submit();
    });

    // setup the Taggable plugin to run in public mode
    Taggable.create('#target-image', { mode : Taggable.MODES.REGISTERED });
});
