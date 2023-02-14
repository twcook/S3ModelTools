"""
The app_gen takes a single data model (DM) and the Django request object to create a responsive web app built on Polymer 2.
This app is a data entry app for the data defined by the model.
"""
import os

from unipath import Path

from django.contrib import messages

from s3mtools.settings import APPGEN_TEMPLATE_DIR, APPLIB_DIR

class AppGen(object):

    def __init__(self, dm, request):
        self.msg = ("Creating App.", messages.INFO)
        self.dm = dm
        self.app_name = dm.title.strip().lower().replace(' ', '-')
        self.app_dir = 's3m-' + self.app_name
        self.app_path = Path(APPLIB_DIR, self.app_dir)
        self.bower_json = bower()







def bower():

    bowerStr = """
    {
  "name": "polymer-starter-kit",
  "authors": [
    "The Polymer Authors"
  ],
  "license": "https://polymer.github.io/LICENSE.txt",
  "dependencies": {
    "app-layout": "PolymerElements/app-layout#^2.0.0",
    "app-route": "PolymerElements/app-route#^2.0.0",
    "iron-flex-layout": "PolymerElements/iron-flex-layout#^2.0.0",
    "iron-iconset-svg": "PolymerElements/iron-iconset-svg#^2.0.0",
    "iron-media-query": "PolymerElements/iron-media-query#^2.0.0",
    "iron-pages": "PolymerElements/iron-pages#^2.0.0",
    "iron-form": "PolymerElements/iron-form#^2.0.0",
    "iron-selector": "PolymerElements/iron-selector#^2.0.0",
    "paper-icon-button": "PolymerElements/paper-icon-button#^2.2.0",
    "paper-button": "PolymerElements/paper-button#^2.0.0",
    "paper-input": "PolymerElements/paper-input#^2.0.0",
    "paper-item": "PolymerElements/paper-item#^2.0.0",
    "paper-listbox": "PolymerElements/paper-listbox#^2.0.0",
    "paper-dropdown-menu": "PolymerElements/paper-dropdown-menu#^2.0.0",
    "neon-animation": "PolymerElements/neon-animation#^2.2.1",
    "web-animations-js": "^2.3.1",
    "polymer": "Polymer/polymer#^2.0.0",
    "webcomponentsjs": "webcomponents/webcomponentsjs#^1.0.0",
    "iron-demo-helpers": "^2.1.0",
    "vaadin-date-picker": "vaadin/vaadin-date-picker#^2.0.7",
    "app-storage": "PolymerElements/app-storage#^2.1.1",
    "paper-radio-group": "PolymerElements/paper-radio-group#^2.2.0",
    "geo-location": "ebidel/geo-location#^2.0.2",
    "iron-icons": "PolymerElements/iron-icons#^2.1.1",
    "vaadin-upload": "vaadin/vaadin-upload#^3.0.2"
  },
  "resolutions": {
    "polymer": "^2.0.0"
  },
  "devDependencies": {
    "web-component-tester": "Polymer/web-component-tester#^6.0.0"
  },
  "private": true
}
    """

    return bowerStr

def polymer():
    polymerStr = """
    {
  "entrypoint": "index.html",
  "shell": "src/my-app.html",
  "fragments": [
    "src/my-view1.html",
    "src/my-view2.html",
    "src/my-view3.html",
    "src/my-view404.html"
  ],
  "sources": [
    "images/**/*",
    "src/**/*"
  ],
  "extraDependencies": [
    "bower_components/webcomponentsjs/*.js",
    "!bower_components/webcomponentsjs/gulpfile.js",
    "manifest.json"
  ],
  "lint": {
    "rules": ["polymer-2"]
  },
  "builds": [
    {
      "preset": "es5-bundled"
    },
    {
      "preset": "es6-bundled"
    },
    {
      "preset": "es6-unbundled"
    }
  ]
}

    """

    return polymerStr
