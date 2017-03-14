from flask import Flask,render_template,send_from_directory,send_file
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
    return 'Namaste .. Pls enter any folder follwed by slash'

@app.route('/<name>')
def displayListOfFile(name):
    name = name.replace(">","/")
    path = '/home/pi/'+name
    if os.path.isdir(path):
        a = list_directory(path)
        name = name.replace("/",">")
        return render_template('index.html',tree=a,name=name,path=path,isFile=isFile)
    ctype = guess_type(path)
    if os.path.isfile(path):
        return send_file(path)

@app.route('/upload', methods=['POST'])
def upload_function(path):
    #file = request.files['file']
    #file.save(os.path.join(path, filename))
    return "bawa file upload ho gye"
          
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
