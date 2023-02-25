from django.db import models
from s3modeltools.settings import AUTH_USER_MODEL

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Project(models.Model):
    """
    Every item created in S3ModelTools must be assigned to a Project when created. 
    All items (except DM) may be reused in multiple DMs. 
    However, this does not change the original Project.
    The Allowed Groups field contains each of the User Groups allowed to see each item with this 
    Project name. The User Group, Open, is assigned to every user. So if you assign the Open group 
    as one of the allowed groups, all S3ModelTools users will see this item.
    """
    prj_name = models.CharField(("project name"), max_length=110, unique=True, db_index=True, help_text=('Enter the name of your project.'))
    description = models.TextField(("project description"), blank=True, help_text=('Enter a description or explaination of an acronym of the project.'))

    def __str__(self):
        return self.prj_name

    class Meta:
        verbose_name = ("Project")
        verbose_name_plural = ("Projects")
        ordering = ['prj_name']


class Modeler(models.Model):
    """
     Provides names and email addresses for the author and contributor sections of the DM Metadata.
     Also contains the default project for the user.
    """
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET(get_sentinel_user),)
    name = models.CharField(("Name"), max_length=110, help_text=('Enter the author name as it should appear in DM metadata.'))
    email = models.EmailField(("Email"), max_length=110, help_text=('Enter the email address as it should appear in DM metadata as an author and/or contributor.'))
    project = models.ForeignKey(Project, verbose_name=("Default Project"), to_field="prj_name", help_text=('Choose your default Project.'), blank=True, null=True, on_delete=models.CASCADE,)
    prj_filter = models.BooleanField(('Filter by Project'), default=True, help_text=('Uncheck this box if want to see choices from all projects. Note that this will very likely have a negative impact on performance.'))

    class Meta:
        verbose_name = "Modeler"
        verbose_name_plural = "Modelers"
        ordering = ['name', 'email']

    def __str__(self):
        return self.name.strip()
