class PaperlessAuthorizationException(Exception):
    def __init__(self, message, error_code, detail=""):
        super(PaperlessAuthorizationException, self).__init__(message)

        self.detail = detail
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return "Paperless Auth Exception: {}  \n\n {}".format(self.message, self.detail)

