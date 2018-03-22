# Timeline Integration

To add timeline tracking to a model:

1. Remove any foreign keys that are linked to the `Module` object as the inherited `TLEntry` object will already contain it. The property to access the module is called `module`.
2. Add the import statements: `from timeline.models.integrate.entry import TLEntry` and `from timeline.register import timeline_register`.
3. Add `TLEntry` to class inherit list.
4. Add `@timeline_register` to the line above the class declaration.
5. Override the `title` method.
5. Run Django migration manager to check that there are any changes.
6. Run the server and test.

### Sample Class
```python
from django.db import models
from timeline.register import timeline_register
from timeline.models.integrate.entry import TLEntry

@timeline_register
class Model(TLEntry):
    # sample field, is not important to model. 
    sample = models.CharField(max_length=20)
    
    def title(self):
        return self.sample
```