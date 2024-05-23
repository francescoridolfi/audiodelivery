from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from audiodelivery.settings import MODELS, _model_defaults

from audiodelivery.utils.time import convert_to_millis


def is_default(typo):
    return MODELS[typo] == _model_defaults[typo]


class AudioChunkAdmin(admin.ModelAdmin):

    def parent(self, obj):
         return obj.parent
    
    parent.short_description = _("Parent")
    
    def start_time(self, obj):
         return convert_to_millis(obj.start_time)
    
    start_time.short_description = _("From (ms)")
    
    def end_time(self, obj):
         return convert_to_millis(obj.end_time)
    
    end_time.short_description = _("To (ms)")

    list_display = [
         "parent",
         "order",
         "start_time",
         "end_time",
    ]

class AudioAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_at",
        "created_by",
        "edited_at",
        "edited_by",
    ]


if is_default("chunk"):
    from audiodelivery.models import AudioChunk
    admin.site.register(AudioChunk, AudioChunkAdmin)
    

if is_default("audio"):
    from audiodelivery.models import Audio
    admin.site.register(Audio, AudioAdmin)