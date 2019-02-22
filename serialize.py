import cPickle

#----------------------------------------------------------------------
def save(obj, path):
    """
    Pickle a Python object
    """
    with open(path, "wb+") as pfile:
        cPickle.dump(obj, pfile)
 
#----------------------------------------------------------------------
def load(path):
    """
    Extracts a pickled Python object and returns it
    """
    data = []
    pfile = open(path, "rb")
    with open(path, "rb") as pfile:
        data = cPickle.load(pfile)
    return data
 

