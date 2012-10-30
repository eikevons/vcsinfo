class VCSError(StandardError):
    pass

class WrongVCS(VCSError):
    pass

class CommandFailed(VCSError):
    pass

class FileNotFound(VCSError):
    pass
