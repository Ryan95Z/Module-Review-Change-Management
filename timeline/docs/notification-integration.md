# Adding custom notifications to system

### Creating a custom notification
Create a file anywhere in your package and import the following:
```
from timeline.utils.notifications.notices import BaseNotice
```

Then create a custom class that overrides the create method. In this method you will be able to provide any number of kwargs to create your notification. For example:
```python
# inherit the BaseNotice
class MentionNotice(BaseNotice):
    def __init__(self):
        # define a template for your notification message
        content_template = "{} mentioned you in a post for {}"
        super(MentionNotice, self).__init__(
            content_template=content_template,
            link_name='discussion'  # the name of the url for the reverse method
        )

    def create(self, **kwargs):
        # provide a number of kwargs that you require to make the notification
        author = kwargs['author']
        entry = kwargs['entry']
        mention_user = kwargs['mention']
        module_code = entry.module_code
        
        # make the content from your data and template
        content = self.content_template.format(author.username, module_code)
        
        # provide the data required to create the redirect url
        url = self.get_url({
            'module_pk': module_code,
            'pk': entry.pk,
        })
        
        # call this method to create the notifications
        self._create_notification(content, mention_user, url)
```
Once this has been created. It now needs to be linked to the timeline notification factory.

### Connecting your notification to the timeline factroy

Create a new file in the root of your package called `setup.py`, then import the following:
```python
from timeline.utils.notifications.factory import NotificationFactory
```
You will also need to import your custom notification as well. Then we add the following lines of code to connect your notification.

```python
NotificationFactory.register(<your_notification_object>, "<key_to_access_it>")
```
You will replace `<your_notification_object>` with your notification object and replace `<key_to_access_it>` with any valid string. This key is used to access the notification later.

Once this has been completed, the file needs to be imported by Django's app configure class. Open the file `apps.py`. There will be a class called `<your_package_nane>Config`. Add the following method to it:
```python
def ready(self):
    import <your_package_name>.setup
```

Next edit your `__init__.py` file in the root of your package and add the following line:
```python
default_app_config = '<your_package_name>.apps.<config_class>'
```
Where the `<config_class>` is the class that is used in `apps.py`. Now run the server to check that everything is working. From here, we can know call the notification from anywhere in the application.

### Creating the notification
Anytime that you require a notification be created, add the following import statement:
```python
from timeline.utils.notifications.helpers import push_notification
```
`push_notification` is a helper function that will create the notification based on the data you provide. Its first param is the key name given to the notification factory. The second parameter is any number of kwargs that you started in the create method. For example:

```python
push_notification(
        "reply",
        discussion=discussion_obj,
        user=request.user,
        parent=discussion['parent']
)
```
where `discussion`, `user` and `parent` are the kwargs that have been set for the reply notification. 