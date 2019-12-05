# Django Observable Models

*NOTE: this is an experimental WIP. It currently will ONLY work when model instances are updated in the same process as model updates occur. Obviously this isn't ideal for most django setups. I'm working on a way to fix this.*

Django Observable Models allows you to subscribe to model operations using rxpy Observables. This is particularly useful for implementing things like GraphQL subscriptions.

## Installation

```bash
$ pip install django-observable-models
```

## Usage

Django Observable Models provides an abstract `ObservableModel` class, which adds observability on that model. It adds a `model_events` method that returns an observable that receives notifications in the following format:

```
{
    "operation": ObservableModel.CREATED or ObservableModel.UPDATED or ObservableModel.DELETED,
    "instance": <your model instance>
}
```

It can be used like so:

```python
# yourapp/models.py
from observable_models.models import ObservableModel

class YourModel(ObservableModel):
    pass

# Subscribe to model creation
YourModel.model_events() \
    .pipe(filter(lamda event: event['operation'] == YourModel.CREATED)) \
    .subscribe(lambda: ...)

# Subscribe to updates on model #12
YourModel.model_events() \
    .pipe(
        filter(lamda event: event['operation'] == YourModel.UPDATED),
        filter(lamda event: event['instance'].pk == 12)
    ).subscribe(lambda: ...)

# Subscribe to model deletion 
YourModel.model_events() \
    .pipe(filter(lamda event: event['operation'] == YourModel.DELETED)) \
    .subscribe(lambda: ...)
```