class PaperlessException(Exception):
    def __init__(self, message, error_code=None, detail=""):
        super(PaperlessException, self).__init__(message)
        self.detail = detail
        self.error_code = error_code
        self.message = message

        def __str__(self):
            return "Paperless Exception: {}".format(self.message)


class PaperlessAuthorizationException(PaperlessException):
    def __init__(self, message, error_code, detail=""):
        super(PaperlessAuthorizationException, self).__init__(message)

    def __str__(self):
        return "Paperless Auth Exception: {}  \n\n {}".format(self.message, self.detail)


class PaperlessNotFoundException(PaperlessException):
    def __init__(self, message, error_code=404, detail=""):
        super(PaperlessNotFoundException, self).__init__(message)

        self.detail = detail
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return "Paperless Resource Not Found: {}  \n\n {}".format(self.message, self.detail)
