"""
.. module:: appserver
    :platform: Linux
    :synopsis: creates an application instance and runs the dev server

.. moduleauthor:: Evan Campbell
"""

if __name__ == '__main__':
    from hydroapi.application import create_app
    app = create_app()
    app.run()