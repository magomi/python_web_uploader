from flask import request, jsonify, Flask
from shutil import copyfileobj
import os
from pathlib import Path

# where to store the files
UPLOAD_FOLDER = os.environ['UPLOAD_FOLDER']

app = Flask(__name__)


@app.route('/upload/<path:path_with_filename>', methods=['PUT'])
def upload(path_with_filename):
  filename = path_with_filename.split('/')[-1]
  rel_path_elements = path_with_filename.split('/')[0:-1]
  full_path = os.path.sep.join([UPLOAD_FOLDER] + rel_path_elements)
  full_file_path = os.path.sep.join([UPLOAD_FOLDER] + rel_path_elements + [filename])

  if not os.path.exists(full_path):
    fs_path = Path(full_path)
    fs_path.mkdir(parents=True)

  with open(full_file_path, 'wb') as f:
    copyfileobj(request.stream, f)
  f.close()

  resp = jsonify({'message': 'uploaded'})
  resp.status_code = 200
  return resp


@app.route('/remove/<path:path_with_filename>', methods=['DELETE'])
def remove(path_with_filename):

  full_file_path = UPLOAD_FOLDER + os.path.sep + path_with_filename

  if os.path.exists(full_file_path):
    os.remove(full_file_path)
    resp = jsonify({'message': 'removed'})
    resp.status_code = 200
    return resp
  else:
    resp = jsonify({'message': 'not found'})
    resp.status_code = 404
    return resp



if __name__ == "__main__":
    app.run(host=os.environ['LISTENING_IF'], port=os.environ['LISTENING_PORT'])
