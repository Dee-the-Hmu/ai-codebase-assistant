"""
to confrim the validated github_url (repo) is public 
get the repo's metadata, default branch and lastest commit sha 
and create CreateRepo Pydantic object
"""
#test run this file only with "python -m services.github.client"

from schemas.config import settings
import requests
from schemas.repository import RepositoryCreate


GITHUB_TOKEN = settings.github_token
BASE_URL = "https://api.github.com"

#this dictionary of extra information will be sent with GitHub API request
HEADERS = {
    "Authorization": f"Bearer {settings.github_token}", #sends your github api token
    "Accept": "application/vnd.github+json", #asks GitHub to return its standard JSON response format 
    "X-GitHub-Api-Version": "2022-11-28", #tells GitHub what REST API version your applicaiton expects 
}

# get the repo
def get_repository(owner : str, repo_name : str) -> dict:
    #creates the url back from the owner and repo_name
    url = f"{BASE_URL}/repos/{owner}/{repo_name}"

    response = requests.get(
        url=url,
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json() # returns a Python dict

# check if the repo is public 
def check_public(repo_response_dict : dict) -> bool: 
    # if repo_response_dict["private"] == True:
    #     return False
    return not repo_response_dict["private"]
   

#make a RepositoryCreate Pydantic Model ready to use
def make_RepositoryCreate_Obj(owner : str, repo_name : str, repo_response_dict : dict) -> RepositoryCreate: 
    github_url = f"https://github.com/{owner}/{repo_name}"
    name = repo_name
    default_branch=repo_response_dict["default_branch"]
    
    commit_response_dict = helper_get_commit_response_dict(owner=owner, repo_name=repo_name, default_branch=default_branch)

    latest_commit_sha = commit_response_dict["sha"]

    ingestion_status = "pending"

    return RepositoryCreate(
        github_url=github_url,
        name=name,
        owner=owner,
        default_branch=default_branch,
        latest_commit_sha=latest_commit_sha,
        ingestion_status=ingestion_status
    )

   
    
# helper function, after we know the default branch, get the latest commit of that branch
def helper_get_commit_response_dict(owner : str, repo_name : str, default_branch : str) -> dict:
     # to get the latest commint SHA secure hash algorithm
    url = f"{BASE_URL}/repos/{owner}/{repo_name}/commits/{default_branch}"
    response = requests.get(
        url=url,
        headers=HEADERS,
        timeout=15
    )
    response.raise_for_status()
    commit_response_dict = response.json()

    return commit_response_dict


#testing
# repository = get_repository(
#     owner="Dee-the-Hmu",
#     repo_name="ai-codebase-assistant",
# )


# print(repository["name"])
# print(repository["default_branch"])
# print(repository["html_url"])

# print(repository)
# """
# ai-codebase-assistant
# master
# https://github.com/Dee-the-Hmu/ai-codebase-assistant
# """

