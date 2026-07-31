from jinja2.nodes import Test
from constants.bitbucket_route_constants.bitbucket_pr_routes import BitBucketPRRoutes
from clients.repositories.bitbucket_integration.bitbucket_pr_client import BitBucketPRClient
from models.schemas.bitbucket_schemas.bitbucket_create_pr import CreatePullRequestRequest, Branch, PullRequestEndpoint, Reviewer 
from models.schemas.bitbucket_response_schemas.bitbucket_create_pr import PullRequestResponse
from models.schemas.bitbucket_response_schemas.bitbucket_approve_pr import PullRequestApprovalResponse

from clients.repositories.bitbucket_integration.bitbucket_repository_client import BitBucketRepositoryClient
from models.schemas.bitbucket_schemas.bitbucket_create_repo import CreateRepositoryRequest, Project, MainBranch
from constants.bitbucket_route_constants.bitbucket_repository_routes import BitBucketRepoRoutes
from models.schemas.bitbucket_response_schemas.bitbucket_create_repository import RepositoryResponse
from models.schemas.bitbucket_schemas.bitbucket_update_repo import UpdateRepositoryRequest, MainBranch, Project
from clients.repositories.github_integration.github_branch_client import GitHubBranchClient
from models.schemas.github_schemas.branch_schema import Branch
from clients.repositories.github_integration.github_commit_client import GitHubCommitClient
from constants.github_route_constants.github_commit_route import CommitRoutes
from models.schemas.github_schemas.commit_variables import CommitIntent, FileAddition
from clients.repositories.github_integration.github_branch_client import GitHubBranchClient

from config.config import settings
#from repositories.github_integration import GitHubCommitClient, GitHubBranchClient
import asyncio as core_asyncio
import structlog

logger = structlog.get_logger()
branch_client = GitHubBranchClient()

async def main():

    WORKSPACE = "ingen-test-workspace"
    REPO_SLUG = "newer-repo-slug"

    request = Branch(
    owner="Max-Sami07",
    repo_name="test-repo-ingen",
    branch_name="test_graphQL"
    )

    file_commit = CommitRoutes.from_file(repo_path="logger.py", local_path="C:\\Users\\User\\Projects\\InGen\\in_gen_backend\\test_endpoint.py")
    data = CommitIntent(
        branch_name="test_graphQL",
        commit_message="Testing Commiting to ghub",
        repository_owner="Max-Sami07",
        repository_name="test-repo-ingen",
        additions=[file_commit],
        deletions=None
    )

    client = GitHubCommitClient(branch_client=branch_client)
    route = CommitRoutes()

    try:
        # url = route.base_url_repo(workspace=WORKSPACE, repo_slug=REPO_SLUG)
        # logger.info("Starting create_commit endpoint...")
        # logger.info(f"URL: {url}")
        result = await client.create_commit(commit_schema=data)
        logger.info(f"Result: {result}")
        # logger.info(f"raw response: {result.json()}")
        #result.raise_for_status()
        # commit_data = RepositoryResponse(**result.json())
        # logger.info(f"Response strctured: {commit_data}")
        logger.info(f"Commit successful!")
    except Exception as e:
        logger.error(f"Commit failed: {e}")
        raise e

if __name__ == "__main__":
    core_asyncio.run(main())

# async def main():
    
#     # 1. Instantiate the client (creates the object)
#     repo_client = GitHubCommitClient()
#     # with open("test.py", "rb") as file:
#     #     encoded_string = base64.b64encode(file.read()).decode('utf-8')
#     # # 2. Setup your data
#     # data = CommitSchema(
#     #     owner="Max-Sami07",
#     #     repo="test-repo-ingen",
#     #     message="Test commit from Ingen Project",
#     #     path="test.py",
#     #     content=encoded_string,
#     #     committer=Committer(
#     #         email="msami@retrorabbit.co.za",
#     #         name="Max-Sami07"
#     #     )
#     # )

#     data = CommitVariables(
#         owner="Max-Sami07",
#         repo="test-repo-ingen",
#         branch="main",
#         commit_message="GraphQL commit test",
#         deletions=None,
#         files= [
#             FileCommit(
#                 path="logger.py",
#                 contents=CommitRoutes.from_file(repo_path=)
#         )],
#         path=None,
#     )

#     # 
#     payload = GraphQLCommitPayload(
#     variables=Variables(
#         input=Input(
#             branch=Branch(
#                 repository_name_with_owner=f"{data.owner}/{data.repo}",
#                 branch_name=data.branch,
#             ),
#             message=Message(headline=data.commit_message),
#             expected_head=ExpectedHead(oid=head_sha),
#             file_changes=FileChanges(
#                 additions=[
#                     FileAddition(path=f.path, contents=f.contents)
#                     for f in data.files
#                 ]
#             ),
#         )
#     )
# )
#     # 


#     try:
#         # 3. AWAIT the method call on the INSTANCE
#         print(f"encoded_string: {data.files[0].contents}")
#         print("Starting Commit Process")
#         #print(f"endpoint: {CommitRoutes.create_repo(owner=data, repo=data.repo, path=data.path)}")
#         # test = await repo_client.put(endpoint=CommitRoutes.create_update_repo(owner=data.owner, repo=data.repo, path=data.path), json=data.model_dump())
#         print(f"GraphQL endpoint: {settings.api.github_graph_ql_endpoint}")
#         test = await repo_client.create_commit(commit_schema=data)
#         print(f"test response: {test.text}")
#         print("Success! Response:")
#     except Exception as e:
#         print(f"Failed to create commit: {e}")

# def build_graphql_payload(commit_schema: CommitVariables, expected_head_sha: str) -> dict:
#     mutation = CommitRoutes.GQL_QUERY
    
#     payload = GraphQLCommitPayload(
#     variables=Variables(
#         input=Input(
#             branch=Branch(
#                 repository_name_with_owner=f"{commit_schema.owner}/{commit_schema.repo}",
#                 branch_name=commit_schema.branch,
#             ),
#             message=Message(headline=commit_schema.commit_message),
#             expected_head=ExpectedHead(oid=head_sha),
#             file_changes=FileChanges(
#                 additions=[
#                     FileAddition(path=f.path, contents=f.contents)
#                     for f in commit_schema.files
#                 ]
#             ),
#         )
#     )
# )

#     return {
#         "query": mutation,
#         "variables": payload
#     }

# if __name__ == "__main__":
#     core_asyncio.run(main())