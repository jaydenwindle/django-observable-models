from django.db import models
from rx import Observable
from rx.subject import Subject
from rx.operators import filter

class ObservableModelQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj._on_delete()
        super(ObservableModelQuerySet, self).delete(*args, **kwargs)


class ObservableModel(models.Model):
    CREATED = 'created'
    UPDATED = 'updated'
    DELETED = 'deleted'

    _subject = Subject()
    objects = ObservableModelQuerySet.as_manager()

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.pk is None:
            self._subject.on_next({
                "operation": self.CREATED,
                "model": self.__class__,
                "instance": self
            })
        else:
            self._subject.on_next({
                "operation": self.UPDATED,
                "model": self.__class__,
                "instance": self
            })

        super(ObservableModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self._on_delete()
        super(ObservableModel, self).delete(*args, **kwargs)
    
    def _on_delete(self):
        self._subject.on_next({
            "operation": self.DELETED,
            "model": self.__class__,
            "instance": self 
        })
    
    @classmethod
    def model_events(cls):
        cls._subject.pipe(filter(lambda event: event['model'] == cls))
