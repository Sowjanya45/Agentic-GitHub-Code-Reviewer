from app.db.database import SessionLocal
from app.db.models import Finding, GitHubAccount, PullRequest, Repository, Review, User


def test_full_relationship_chain_roundtrip():
    db = SessionLocal()
    try:
        user = User(login="octocat")
        user.github_account = GitHubAccount(github_user_id=1)
        repo = Repository(github_repo_id=10, full_name="octocat/hello", user=user)
        pr = PullRequest(number=1, title="Fix bug", repository=repo)
        review = Review(pull_request=pr)
        review.findings.append(
            Finding(agent="bug", category="BUG", severity="LOW", confidence=0.5, file="a.py",
                    line_start=1, line_end=2, title="t", problem="p", evidence=["e"], recommendation="r")
        )
        db.add(user)
        db.flush()
        assert review.status == "QUEUED" and review.findings[0].status == "VALID"
        assert review.findings[0].evidence == ["e"]
    finally:
        db.rollback()  # leave the database clean
        db.close()
