# Audio Delivery
A Django Application to manage the backend features for a Streaming Project.

## What it does?
The application aims to manage the uploading of audio files by users, split them into multiple chunks and generate the APIs to obtain information and chunks from the latter.
The chunks will not uploaded into your **media** dir in order to prevent unauthorized access from users.

## Features
- Customize your Audio and AudioChunk Models and Serializers
- Customize Permissions presences and names
- Choose the saving folder
- Choose the format types

## Settings Examples:
By defaults the settings are:
```python
# Audio Delivery Settings

AUDIODELIVERY_CHUNK_DIR = BASE_DIR / "chunks"

AUDIODELIVERY_ALLOWED_FORMATS = (".mp3", )

AUDIODELIVERY_CHUNK_MODEL = "audiodelivery.AudioChunk"
AUDIODELIVERY_AUDIO_MODEL = "audiodelivery.Audio"

AUDIODELIVERY_PERMISSIONS = {
    "retrieve": ("can_retrieve", _("Can User retrieve Audio infos")),
    "upload": ("can_upload", _("Can User upload new Audio"))
}

AUDIODELIVERY_CHUNK_SERIALIZER = "audiodelivery.api.serializers.AudioChunkSerializer"
AUDIODELIVERY_AUDIO_SERIALIZER = "audiodelivery.api.serializers.AudioSerializer"
```

But you can create your custom Audio model by importing the Base Abstract Model from: **audiodelivery.models.audio.BaseAudio**
For example:
```python
from django.db import models
from audiodelivery.models.audio import BaseAudio, PERMISSIONS

class MyAudio(BaseAudio):
    class Meta:
        verbose_name = "MyAudio"
        verbose_name_plural = "MyAudios"

        permissions = list()

        if "retrieve" in PERMISSIONS:
            permissions.append(PERMISSIONS["retrieve"])
        
        if "upload" in PERMISSIONS:
            permissions.append(PERMISSIONS["upload"])

        permissions = tuple(permissions)

    # custom fields go here
    genre = models.CharField("Genre", max_length=255)
    ...
```

And next you've to update the settings.py file with:
```python
...
AUDIODELIVERY_AUDIO_MODEL = "your_app_label.MyAudio"
...
```

## Installing
First of all AudioDelivery requires two extra packages:
- [django-rest-framework](https://www.django-rest-framework.org/#installation) -> for manage the REST APIs requests
- [django-crum](https://pypi.org/project/django-crum/) -> a middleware for obtain the current user in the thread

Make sure that you've installed apps and middleware in the **settings.py** file:
```python
INSTALLED_APPS = [
    # other apps...
    'rest_framework',
    'audiodelivery',
]
...
MIDDLEWARE = [
    # other middlewares...
    'crum.CurrentRequestUserMiddleware',
]
```

Next step is to append in the settings file, the default AudioDelivery Settings showed [before this section](#settings-examples), and follow the previous tutorial if you want to implement custom models/serializers, then run:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Now you can run the project!
