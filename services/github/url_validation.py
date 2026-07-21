
"""
validate the github url
extract owner and repo name
"""
from urllib.parse import urlparse

def validate_and_parse_github_url(github_url : str) -> tuple[str, str, str]:
    
    #removes unnecessary spaces and a trailing / from the github_url
    normalized_url = github_url.strip().rstrip("/") #rstrip("/") removes / characters from the end 

     #github repo url can be provided in 2 forms: https://github.com/user/repo or https://github.com/user/repo.git
     #remove .git at the end 
    if normalized_url.endswith(".git"):
        normalized_url = normalized_url[:-4] #keeps evertying except the last 4 characters

    #use urlparse from urllib to check "https" and "github.com" and to get "/user/repo" easily
    parsed_url = urlparse(normalized_url)

    #validate
    if parsed_url.scheme != "https":
        raise ValueError("GitHub URL must use HTTPS")
    if parsed_url.netloc not in {"github.com", "www.github.com"}:
        raise ValueError("URL must be a GitHub URL")
    
    # get owner and repo from parsed_url.path
    path_parts = []

    # parsed_url.path returns "/user/repo"
    for part in parsed_url.path.split("/"): #["", "user", "repo"] 
        if part: 
            path_parts.append(part)  #["user", "repo"]
    
    if len(path_parts) != 2:
        raise ValueError("URL must point directly to a GitHub repository")
    
    owner, repo_name = path_parts

    return (owner, repo_name, normalized_url)

