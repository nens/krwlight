# Experimental code, trying out something to make lizard-ui more
# composition-based instead of the inheritance-hierarchy-from-hell that it is
# now.


class BaseLayout(object):

    def __init__(self, view):
        self.view = view
        self.request = self.view.request

    base_template = 'krwlight/base.html'
