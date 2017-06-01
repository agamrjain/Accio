from flask import Flask,render_template,send_from_directory,send_file,request,redirect
#from werkzeug import secure_filename
import os
import posixpath
import mimetypes
import urllib
import cgi
import sys
import shutil

app = Flask(__name__)

default_path = '/media/pi/'


@app.route('/settings', defaults={'path':default_path})
@app.route('/<path:path>/settings')
def setting(path):
    return render_template('settings.html')


@app.route('/settings_form/',  methods=['POST'])
def settings_form():
    global default_path
    default_path = '/media/pi/'
    dir=request.form['dir']
    default_path = dir
    return redirect("/")


@app.route('/', defaults={'name': 'some_unknown_folder_path'})
@app.route('/<path:name>')
def display_list_of_file(name):
    name = "/"+name
    global default_path
    if name == '/some_unknown_folder_path':
        name = default_path
    path = name
    if os.path.isdir(path):
        a = list_directory(path)
        path = path.replace('/','//')
        path = path.replace('////', '//')
        path_list = path.split('//')

        list_of_links = ['/']
        i=0
        for link in path_list:
            list_of_links.append(list_of_links[i] + "/" + link)
            i=i+1
        list_of_links.remove('/')
        return render_template('index_material3.html',file_list=a,name="/"+name,path=path,isFile=isFile, rootpath=app.root_path,path_list=path_list,list_of_links=zip(list_of_links,path_list))
    elif os.path.isfile(path):
        return send_file(path)
    else:
        return render_template('error.html',name=name)


@app.route('/upload_form/', methods = ['GET', 'POST'])
def upload_form():
    if request.method == 'POST':
        f = request.files['file']
        path = request.form['path']
        f.save(os.path.join(path, f.filename))
        return redirect("/"+path)
    else:
        return "invalid Request"


def isFile(fileName):
    return os.path.isfile(fileName)


def list_directory(path):
        try:
            list = os.listdir(path)
        except os.error:
            return "404, No permission to list directory"
        #list.sort(key=lambda a: a.lower())
        return list

def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.
        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)
        """
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path


def guess_type(path):
        """Guess the type of a file.
        Argument is a PATH (a filename).
        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.
        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.
        """

        base, ext = posixpath.splitext(path)
        if ext in extensions_map:
            return extensions_map[ext]
        ext = ext.lower()
        if ext in extensions_map:
            return extensions_map[ext]
        else:
            return extensions_map['']

if not mimetypes.inited:
    mimetypes.init() # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
