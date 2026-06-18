class BranchRoutes:
    BASE = "/repos/{owner}/{repo}/branches"
    MERGES = "/repos/{owner}/{repo}/merges"

    @classmethod
    def list(cls, owner: str, repo: str) -> str:
        return cls.BASE.format(owner=owner, repo=repo)

    @classmethod
    def get(cls, owner: str, repo: str, branch_name: str) -> str:
        return f"{cls.list(owner, repo)}/{branch_name}"

    @classmethod
    def merge(cls, owner: str, repo: str) -> str:
        return cls.MERGES.format(owner=owner, repo=repo)