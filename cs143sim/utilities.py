"""This module contains all utility definitions.

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""


def full_string(thing):
    """Return a full string representation of `thing`, such that iterables with
    objects and nested iterables can be printed informatively

    :param thing: any iterable (or otherwise) to stringify
    :return: nested string representation of `thing`
    :rtype str:
    """
    if type(thing) == dict:
        return ', '.join(full_string(key) + ' : ' + full_string(thing[key])
                         for key in thing)
    if type(thing) == list:
        return '[' + ', '.join(full_string(item) for item in thing) + ']'
    if type(thing) == tuple:
        return '(' + ', '.join(full_string(item) for item in thing) + ')'
    else:
        return str(thing)


def print_event(event):
    """Print a description for `event`

    :param event: any :class:`~simpy.events.Event`
    """
    print 'At', event.env.now, event.__class__.__name__, 'for',
    print full_string(event.actor)
