from flask import Flask,render_template,send_from_directory,send_file,request,redirect
from werkzeug import secure_filename
import os
import posixpath
import mimetypes
import urllib
import cgi
import sys
import shutil

app = Flask(__name__)

@app.route('/')
def index():    
    return '<h2>Namaste .. Pls enter any folder followed by slash</h2>'+ app.root_path

@app.route('/<name>')
def displayListOfFile(name):
    name = name.replace(">","/")
    path = name
    if os.path.isdir(path):
        a = list_directory(path)
        name = name.replace("/",">")
        nameitem = name.split('>')
        linkname=''
        return render_template('index_material3.html',tree=a,name=name,path=path,isFile=isFile, nameitem = nameitem,linkname = linkname, rootpath=app.root_path)
    ctype = guess_type(path)
    if os.path.isfile(path):
        return send_file(path)
    
@app.route('/uploader/', methods = ['GET', 'POST'])
def upload_file():
   #name = name.replace(">","/")
   if request.method == 'POST':
      f = request.files['file']
      path = request.form['path']
      name = request.form['name']
      f.save(os.path.join(path, f.filename))
      #f.save(secure_filename(f.filename))
      location = '/'+name
      return redirect(location, code=302)
      
def isFile(fileName):
    return os.path.isfile(fileName)

def list_directory(path):
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
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
