# create_superuser.py
from django.contrib.auth import get_user_model

User = get_user_model()

username = "osbornm"
email = "osbornm300@gmail.com"
password = "Qwerty123Mo!"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("Superuser created ✅")
else:
    print("Superuser already exists 🚀")