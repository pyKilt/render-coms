
from flask import Flask, jsonify, request
from flask_accept import accept
from premailer import transform

# from jinja2 import Template

import os
import os.path
import jinja2

# https://stackoverflow.com/questions/38642557/how-to-load-jinja-template-directly-from-filesystem
templateLoader = jinja2.FileSystemLoader( searchpath="./templates/")
templateEnv = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@accept('text/html')
def get_html(path):
    template_file = path.strip('/') + '.html'
    print os.getcwd() + '/' + template_file

    # print request.headers
    # all_args = request.args.to_dict()
    # return jsonify(all_args)

    if os.path.exists( os.getcwd() + '/templates/' + template_file ):
        try:
            # return transform( templateEnv.get_template( template_file ).render( request.args.to_dict() ) )
            return transform( open( os.getcwd() + '/templates/' + template_file, 'r').read() )
        except Exception, e:
            return str(e), 500

    return 'path: %s does not exist' % path, 404

if __name__ == '__main__':
    app.run()
