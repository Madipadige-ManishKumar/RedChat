import os 
from github  import Github,Auth
from dotenv import load_dotenv

load_dotenv()

github_token  = os.getenv("github_token")

auth = Auth.Token(github_token)
g = Github(auth=auth)

user = g.get_user()

def create_repo(repo_name:str,description:str=None,private:bool=True,has_issues:bool=False):
    try:
        repo = user.create_repo(
            name=repo_name,
            description=description,
            private=private,
            has_issues=has_issues,
        )
        return f"✅ Repository '{repo_name}' created successfully."
        
    except Exception as e:
        return f"❌ Error creating repository: {e}"
        

def create_issue(repo_name:str,title:str,body:str=None):
    try:
        repo = user.get_repo(repo_name)
        issue = repo.create_issue(
            title=title,
            body=body,
        )
        return f"✅ Issue '{title}' created successfully."
    except Exception as e:        
        return f"❌ Error creating issue: {e}"