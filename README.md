# Django Observable Models

Django Observable Models allows you to subscribe to model operations using rxpy Observables. This is particularly useful for implementing things like GraphQL subscriptions.

## Installation

```bash
$ pip install django-observable-models
```

## Usage

```python
# yourapp/models.py
from observable_models.models import ObservableModel

class YourModel(ObservableModel):
    pass

# Subscribe to model creation
YourModel.model_events.pipe(filter(lamda event: event['operation'] == YourModel.CREATED))

# Subscribe to model updates 
YourModel.model_events.pipe(filter(lamda event: event['operation'] == YourModel.UPDATED))

# Subscribe to model deletion 
YourModel.model_events.pipe(filter(lamda event: event['operation'] == YourModel.DELETED))
```