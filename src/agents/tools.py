from src.slack import service as slack_service 
from  typing import List,Optional
from src.rag.reteriver import query_vector_db
from src.MCP.Github import service as github_service

def get_slack_context(mode:str,channels:Optional[List[str]]=None):
    '''
        This function get_slack_context takes  2 modes 

        1 =  all = > which fetches the history of all channels the bot is a member of
        2 = specific => which fetches the history of specific channels provided in the channels list

        channel => is used to  specify the channels and it is null when the mode is all
    '''
    print(f"Fetching Slack context with mode: {mode} and channels: {channels}")
    if mode == "all":
        return slack_service.get_all_joined_channels_history()
    elif mode == "specific" and channels:
        return slack_service.get_multiple_channels_history(channels)
def send_slack_message(mode:str,text:str,channel:Optional[List[str]] = None):
    '''
    send Msg to channel it can be specific or all
    '''
    print(f"Sending Slack message with mode: {mode}, text: {text}, and channel: {channel}")
    if mode == "all":
        return slack_service.post_to_all_channels(text)
    elif mode == "specific" and channel:
        return slack_service.post_to_multiple_channels(channel, text)

def query_vector_db_tool(mode:str,query:str,channel_names:Optional[List[str]]):
    '''
        This function get_slack_context takes  2 modes 

        1 =  all = > which fetches the history of all channels the bot is a member of
        2 = specific => which fetches the history of specific channels provided in the channels list

        channel => is used to  specify the channels and it is null when the mode is all
    '''
    if mode == "all":
        channel_names = slack_service.get_all_joined_channels()
    elif mode == "specific" and channel_names:
         channel_names = channel_names
    print(f"Querying vector DB with query: {query} and channel_names: {channel_names}")
    return query_vector_db(query, channel_names)

def create_github_issues(title:str,body:str):
    '''
        This function creates a github issue with the provided title, body, and labels.
    '''
    print(f"Creating GitHub issue with title: {title}, body: {body}")
    return github_service.create_issue(title, body)

def  create_repo(name:str,description:str,private:bool):
    '''
        This function creates a github repository with the provided name, description, and private status.
    '''
    print(f"Creating GitHub repository with name: {name}, description: {description}, and private: {private}")
    return github_service.create_repo(name, description, private)



TOOLS =[ 
    get_slack_context,
    send_slack_message,
    query_vector_db_tool,
    create_github_issues,
    create_repo
]


