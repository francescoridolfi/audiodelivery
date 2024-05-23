from rest_framework import serializers

def convert_to_millis(time_data) -> int:
    """
    Method for convert datetime.time object into milliseconds 
    
    Args:
        time_data: accept only an instance of datetime.time class

    Returns:
        Converting object for hours minutes and seconds into milliseconds
    """
    return  int((
                (
                    time_data.hour * 60 + time_data.minute
                ) * 60 + time_data.second
            ) * 1000 + time_data.microsecond / 1000)


HOURS_CHUNK = 60*60*1000
MINUTES_CHUNK = 60*1000
SECONDS_CHUNK = 1000

def convert_from_millis(milliseconds: int) -> str:
    """
    Method for convert milliseconds into a time iso format

    Args:
        milliseconds: accept only int values

    Returns:
        A string with the value translated in iso format
    """

    hours = int(milliseconds / HOURS_CHUNK)
    h_prefix = '0' if hours < 10 else ''

    rest = milliseconds - (hours * HOURS_CHUNK)

    minutes = int(rest / MINUTES_CHUNK)
    m_prefix = '0' if minutes < 10 else ''

    rest -= (minutes * MINUTES_CHUNK)

    seconds = rest / SECONDS_CHUNK
    s_prefix = '0' if seconds < 10 else ''

    return f"T{h_prefix}{hours}:{m_prefix}{minutes}:{s_prefix}{seconds}"


class TimeToMillisField(serializers.TimeField):
    """
    Serializer Field class for represent a datetime.time object into milliseconds
    """
    def to_representation(self, value):
        if value in (None, ""):
            return None
        
        return convert_to_millis(value)