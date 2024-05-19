def convert_to_millis(time_data):
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
    