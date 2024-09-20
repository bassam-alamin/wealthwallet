
def get_or_none(classmodel, **kwargs):
    """
    Interface class to get the object or return None
    :param classmodel:
    :param kwargs:
    :return:
    """
    try:
        return classmodel.objects.get(**kwargs)
    except Exception as error:
        return None
