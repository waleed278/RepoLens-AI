class InvalidRepositoryURLError(Exception):
    pass


class GitHubRepositoryNotFoundError(Exception):
    pass


class GitHubRateLimitError(Exception):
    pass


class GitHubServiceError(Exception):
    pass

class AIServiceError(Exception):
    pass

class AIInvalidResponseError(Exception):
    pass

class AnalysisNotFoundError(Exception):
    pass