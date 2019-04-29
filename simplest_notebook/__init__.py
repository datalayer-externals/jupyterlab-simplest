"""
An example demonstrating a stand-alone "notebook".

Copyright (c) Jupyter Development Team.
Distributed under the terms of the Modified BSD License.

Example
-------

To run the example, see the instructions in the README to build it. Then
run ``python main.py``.

"""
import os
from jinja2 import FileSystemLoader
from notebook.base.handlers import IPythonHandler, FileFindHandler
from notebook.notebookapp import NotebookApp
from notebook.utils import url_path_join as ujoin
from traitlets import Unicode

HERE = os.path.dirname(__file__)

class PageHandler(IPythonHandler):
    """
    Serve a notebook file from the filesystem in the notebook interface
    """
    def get(self, kind, notebook_path):
        """Get the main page for the application's interface."""
        page_title = os.path.basename(notebook_path).replace(".ipynb", "")
        # Options set here can be read with PageConfig.getOption
        config_data = {
            # Use camelCase here, since that's what the lab components expect
            'baseUrl': self.base_url,
            'token': self.settings['token'],
            'notebookPath': notebook_path,
            'bundleUrl': ujoin(self.base_url, 'build/'),
            # FIXME: Don't use a CDN here
            'mathjaxUrl': "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js",
            'mathjaxConfig': "TeX-AMS_CHTML-full,Safe",
            'kind': kind
        }
        return self.write(
            self.render_template(
                'index.html',
                static=self.static_url,
                base_url=self.base_url,
                page_title=page_title,
                config_data=config_data
            )
        )

    def get_template(self, name):
        loader = FileSystemLoader(HERE)
        return loader.load(self.settings['jinja2_env'], name)

def _jupyter_server_extension_paths():
    return [{
        'module': 'simplest_notebook',
    }]

def load_jupyter_server_extension(nbapp):
    base_url = ujoin(nbapp.web_app.settings['base_url'], 'simplest')
    handlers = [
        (ujoin(base_url, r'notebooks/(.*)?'), PageHandler),
        (ujoin(base_url, r"build/(.*)"), FileFindHandler,
            {'path': os.path.join(HERE, 'build')})
    ]
    nbapp.web_app.add_handlers('.*$', handlers)