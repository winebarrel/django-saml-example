from djangosaml2.backends import Saml2Backend
from django.contrib.auth.models import Group

class ModifiedSaml2Backend(Saml2Backend):
    def save_user(self, user, *args, **kwargs):
        user.save()
        user_group = Group.objects.get(name='default')
        user.groups.add(user_group)
        user.is_staff = True
        return super().save_user(user, *args, **kwargs)
