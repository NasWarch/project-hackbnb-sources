# Sécurité — Correctifs appliqués

Ce dépôt contient les correctifs des 8 vulnérabilités identifiées dans le rapport
de test d'intrusion du 3 au 5 juin 2026, et exploitées lors de l'incident du
7 novembre 2026.

| ID | Vulnérabilité | Fichier | Correctif |
|----|---------------|---------|-----------|
| **D1** | Injection SQL sur la liste des chambres | `back/api/rooms/rooms_api.py` | Requête paramétrée via l'ORM (`Room.category == category`) au lieu d'une concaténation dans `text()`. |
| **D2** | Lecture arbitraire de fichier (path traversal) | `back/api/uploads/uploads_api.py` | `send_from_directory` + validation du nom (pas de séparateur, pas de `..`, extensions d'image uniquement). |
| **D3** | SSRF sur la route des réservations | `back/api/bookings/bookings_api.py`, `back/services/stripe.py` | Validation stricte de `checkout_session_id` (`^cs_[A-Za-z0-9_]{10,120}$`) **et** encodage de la valeur avant insertion dans l'URL Stripe. |
| **D4** | Génération vulnérable de secret | `back/api/bookings/bookings_api.py` | Remplacement de `sha512(int(time.time()))` par `secrets.token_urlsafe(32)` (256 bits d'entropie). |
| **D5** | Exposition de l'e-mail des hôtes | `back/api/users/users_models.py`, `back/api/rooms/rooms_models.py` | Ajout de `User.to_public_dict()` (sans e-mail), utilisé par `Room.to_dict()`. |
| **D6** | Clé API en clair dans le dépôt | `docker-compose.yml`, `.env.example`, `.gitignore` | La clé est lue depuis `${STRIPE_API_KEY}` (fichier `.env` non versionné). |
| **D7** | En-têtes de sécurité manquants | `apache/apache-prod.conf`, `apache/apache-dev.conf` | Ajout de CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`, HSTS. |
| **D8** | Divulgation dans les en-têtes | `back/app.py`, `back/config.py`, `apache/*.conf` | Debug Flask désactivé par défaut, `ServerTokens Prod`, `ServerSignature Off`, suppression de `X-Powered-By` et de la bannière `Server`. |

## Correction complémentaire recommandée

Les mots de passe sont hachés en **MD5 sans sel** (`back/api/users/users_models.py`).
Ce point n'apparaît pas dans le rapport d'audit mais doit être corrigé :
migration vers `werkzeug.security.generate_password_hash` (scrypt) puis
ré-hachage progressif à la connexion des utilisateurs.

## Points d'exploitation (preuves)

Les captures d'écran et les GIF d'exploitation sur l'environnement de
pré-production sont joints à la synthèse technique déposée sur e-Campus.
