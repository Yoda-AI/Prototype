class DataFormatter(object):
    def __init__(self, obj):
        self.obj = obj

    def get_as_html(self):
        return self.obj.get_as_html()