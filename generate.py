from network.models import *

users = ["hermione", "david", "sana", "adrian", "arthur", "harry"]

for user in users:
    user = User.objects.create_user(user, f"{user}@example.com", "Characters12345!")
    user.save()
    
