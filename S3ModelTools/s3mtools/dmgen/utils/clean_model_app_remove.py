"""
 After deleting apps or models, you will still have remnants of your models in the ContentType table, like permissions related to the deleted models.

To clean these tables, write in DEL_APPS the apps that were deleted, and in DEL_MODELS the models that were deleted and that do not belong to any of the deleted apps. 
Moreover, note that the models have to be written in lowercase.

Finally, we just need to run our script with
$ python manage.py shell
>>> from dmgen.utils.clean_model_app_remove import cleanup
>>> cleanup()

"""
from django.contrib.contenttypes.models import ContentType

def cleanup():
        
    # List of deleted apps
    DEL_APPS = ["users", "records", "msapps"]
    # List of deleted models (that are not in the app deleted) In lowercase!
    DEL_MODELS = []
    
    ct = ContentType.objects.all().order_by("app_label", "model")
    
    for c in ct:
        print(c)
        if (c.app_label in DEL_APPS) or (c.model in DEL_MODELS):
            print("Deleting Content Type %s %s" % (c.app_label, c.model))
            c.delete()
    
