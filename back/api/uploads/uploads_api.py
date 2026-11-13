import os

from flask import Blueprint, request, send_from_directory, abort

uploads_api = Blueprint('uploads', __name__)

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}


@uploads_api.route('/')
def get_upload():
   """
   Renvoie une image du repertoire uploads/.

   FIX D2 : on n'accepte qu'un nom de fichier simple (pas de separateur de
   repertoire, pas de '..') et une extension d'image. send_from_directory
   refuse en plus toute tentative de remontee hors du repertoire.
   """
   name = request.args.get("name", "")

   if (
      not name
      or os.path.basename(name) != name
      or os.path.splitext(name)[1].lower() not in ALLOWED_EXTENSIONS
   ):
      abort(404)

   return send_from_directory('uploads', name)
