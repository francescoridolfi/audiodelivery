import importlib

def import_module_from_string(path_string: str):
    """
    Method for import module from python file

    Args:
        path_string: accept only str values following the format "module.to.module.ClassName"

    Returns:
        Will return the class/method loaded and ready to use
    """
    
    module_name, attr_name = path_string.rsplit(".", 1)
    
    module = importlib.import_module(module_name)
    
    return getattr(module, attr_name, None)