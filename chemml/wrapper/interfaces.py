import importlib



def get_api(name, library, module):
    """
    This function import a python library and obtain a specific class or function of it by string names.

    Parameters
    ----------
    name: str
        name of the function/class

    library: str
        name of python library

    module: str
        name of the library's module that house the function/class

    Returns
    -------
    tuple
        a tuple of two elements: function/class and their type: 'function'/'class'

    """
    if len(module.strip()) > 0:
        full_module_name = library + "." + module
    else:
        full_module_name = library

    themodule = importlib.import_module(full_module_name)

    api = getattr(themodule, name)

    # must be either class or function
    if isinstance(api, type):
        api_type = 'class'
    else:
        api_type = 'function'

    return (api, api_type)


def get_method(obj, method):
    """
    This function get an instance of a class and obtain a specific method of it by its string name.

    Parameters
    ----------
    obj: instance of a class
        An instance of a class

    method: str
        name of the method

    Returns
    -------
    function
        The method function of the received class.

    """
    return getattr(obj, method)


def get_attributes(obj, attr):
    """
    This function get outputs of a class as a dictionary and substitute values with actual class attributes.

    Parameters
    ----------
    obj: instance of a class
        An instance of a class

    outputs: dict
        A dictionary of class outputs.

    Returns
    -------
    dict:
        A dictionary of class attributes upon request.

    """
    return getattr(obj, attr)


def evaluate_param_value(param_val):
    """
    evaluate the string input value to python data structure

    Parameters
    ----------
    param_val: str
        an entry of type str

    Returns
    -------
    bool
        True if the input can become an integer, False otherwise

    Notes
    -----
    returns 'type' for the entry 'type' since type is a reserved word
    """
    try:
        val = eval(param_val)
        if isinstance(val, type):
            return param_val
        else:
            return val
    except:
        return param_val


def evaluate_inputs(inputs, stack, typ='function'):
    """
    This function get a dictionary of inputs and the stack obj to return the parameters and their values.

    Parameters
    ----------
    inputs: dict
        The dictionary of input parameters to a class or function.

    stack: instance of Stack class
        The only container of the entire send/recv token data in the wrapper.

    Returns
    -------
    dict
        A dictionary of all input parameters with their values.

    """
    args = None
    obj = None
    for var in inputs:
        val = evaluate_param_value(inputs[var])
        if isinstance(val, str) and val[0] == '@' and val.count('@') % 2 == 0:
            temp = val.strip().split('@')[1:]  # "@ID2@df" >> ['', 'ID2', 'df']
            val_array = []
            for item in zip(temp[0::2], temp[1::2]):
                val_array.append(stack.pull(item))
            if var == "*args":
                args = val_array
            elif var == "obj" and typ == "class":
                obj = val_array[0]
            else:
                if len(val_array)==1:
                    val = val_array[0]
                else:
                    val = val_array
        inputs[var] = val

    if args is not None:
        del inputs['*args']

    if obj is not None:
        del inputs['obj']

    return {'kwargs':inputs, 'args':args, 'obj': obj}


