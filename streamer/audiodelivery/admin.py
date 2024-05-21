from django.contrib import admin

from django.conf import settings

from audiodelivery.models.getter import VARIABLES, DEFAULTS


def is_default(typo):
    return getattr(settings, VARIABLES[typo], DEFAULTS[typo]) == DEFAULTS[typo]


if is_default("chunk"):
    from audiodelivery.models import AudioChunk
    @admin.register(AudioChunk)
    class AudioChunkAdmin(admin.ModelAdmin):
        pass

if is_default("audio"):
    from audiodelivery.models import Audio
    @admin.register(Audio)
    class AudioAdmin(admin.ModelAdmin):
        pass