
from flask import Flask, jsonify, request
# from flask_accept import accept
from qserious import deserialize
from markdown import markdown
from premailer import Premailer
# from premailer import transform
# from pdfs import create_pdf

# from jinja2 import Template

# import ipdb
import os
import os.path
import jinja2
import re
import yaml

# https://stackoverflow.com/questions/38642557/how-to-load-jinja-template-directly-from-filesystem
templateLoader = jinja2.FileSystemLoader( searchpath="./templates/")
templateEnv = jinja2.Environment( loader=templateLoader )

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_html(path):
    template_file = path.strip('/')
    template_path = os.getcwd() + '/templates/' + template_file

    if os.path.exists( template_path + '.html' ):
        template_format = 'html'
        template_src = templateEnv.get_template( template_file + '.html' )
    elif os.path.exists( template_path + '.md' ):
        template_format = 'md'
        template_src = templateEnv.get_template( template_file + '.md' )
    else:
        return 'path: %s does not exist' % path, 404

    print template_path

    # print request.headers
    # ipdb.sset_trace()
    result = ''

    try:
        result = template_src.render(
            request.get_json() if request.method == 'POST' else deserialize(request.query_string)
        )
    except Exception, e:
        return jsonify({ 'message': str(e) }), 400

    if( template_format == 'md' ):
        template_options = {}
        matched = re.match(r'^---([\s\S]*?)---', result)

        if( matched ):
            template_options = yaml.load( matched.group(1) )

        result = markdown( re.sub(r'^---[\s\S]*?---', '', result) )

        if( 'layout' in template_options ):
            md_block = r'{% extends "layout/' + template_options['layout'] + '.html" %}{% block ' + \
                ( template_options.block if 'block' in template_options else 'main' ) + \
                ' %}' + result + '{% endblock %}'
            result = jinja2.Environment( loader=templateLoader ).from_string(md_block).render()

    if( request.args.get('css') == 'email' ):
        # https://premailer.io/
        result = Premailer(result, keep_style_tags=True).transform()

    # if( request.args.get('format') == 'pdf' ):
    #     return create_pdf(result)

    return result

if __name__ == '__main__':
    app.run()
