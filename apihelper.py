# Week 2: introspection (DIP Ch 4)
# apihelper.py


def info(object, spacing=10, collapse=1):
    """
    Print methods and doc strings
    Takes module, class, list, dictionary, or string
    """
    methodList = [method for method in dir(object) if callable(getattr(object, method))]
    # and-or trick (ifelse() in R) whereby collapse=1 causes the first lambda function to execute, second otherwise
    # join(split(...)) to normalize whitespace
    processFunc = collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print "\n".join("%s %s" %
                    (method.ljust(spacing),
                    processFunc(str(getattr(object, method).__doc__)))
                    for method in methodList)


if __name__ == '__main__':
    print info.__doc__
