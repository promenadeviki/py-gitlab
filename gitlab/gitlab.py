# -*- coding: utf-8 -*-
import http.client as httplib # Httplib was changed to http.client in python3
import requests
import os
import sys
from decouple import config
from decorators import namespace
from exceptions import GitLabServerError
from flask import Flask, request
from flask_restful import Api
from slack_sdk import WebClient
from slack_bolt import App, Say
from slack_bolt.adapter.flask import SlackRequestHandler



#if not os.path.exists(".env"):
#    print('No config files found. Please add tokens to .env. Exiting..')
#    sys.exit(1)


slack_bot_token = config('SLACK_BOT_TOKEN')
slack_sign_secret = config('SLACK_SIGNING_SECRET')

app = Flask(__name__)

bolt_app = App(token=slack_bot_token, signing_secret=slack_sign_secret)

def base_url():
    """Set the GitLab API base URL."""
   # protocol = 'https' if self.use_ssl else 'http'
   # base_url = '{protocol}://{host}/api/{version}'.format(
   #     protocol=protocol, host=self.host, version=self.Version
   # )
    base_url = "https://gitlab.com/api/v4"
    return base_url


class GitLab(object):
    # Use v4 gitlab api version. Others are deprecated in Python
    Version = 'v4'
    ResponseError = GitLabServerError
    client = WebClient(slack_bot_token)
    handler = SlackRequestHandler(bolt_app)

    def __init__(self, host=None, private_token=None, use_ssl=True):
        '''
        Uses decouple to parse .env file and also sets gitlab.com host
        '''
        self.host = host
        self.use_ssl = use_ssl
        private_token = config('TOKEN') #GitLab Token
        self.set_headers(private_token)

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.host)

    def __repr__(self):
        return self.__str__()

    def set_headers(self, private_token):
        """Set `PRIVATE_TOKEN` HTTP request header for restricted endpoints."""
        self.session = requests.Session()
        # Set HTTP `Authorization` request header for the `Session` object
        self.session.headers.update({
            'PRIVATE-TOKEN': '{private_token}'.format(
                private_token=private_token
            )
        })


    def request(self, method, url, data={}, **kwargs):
        """Wrapper method for making requests to endpoints."""
        url = "https://gitlab.com/api/v4"
        print(url)
        print(method, url, kwargs, data)
        #res = self.session.request(method, url, params=kwargs, data=data)

        res = self.session.request('GET', 'https://gitlab.com/api/v4', params=kwargs, data=data)
        if res.status_code not in [200, 201]:
            raise self.ResponseError(res.status_code, res.reason)
        if res.headers['Content-Type'] != 'application/json':
            # The response always returns 200 OK even if it contains redirects
            # If the response `history` attribute is `True` assume
            # 400 Bad Request
            raise self.ResponseError(httplib.BAD_REQUEST,
                                     httplib.responses[httplib.BAD_REQUEST])
        try:
            return res.json()
            msg = "JSON object can't be deserialized"
        except ValueError as e:
            # JSON object can't be deserialized
            # raise exception
            print("ValueError Exception!", msg)


git = GitLab(host='gitlab.com')

def get_users(**kwargs):
    """Get a list of users."""
    path = '/users'
    data = git.request('GET', path, **kwargs)
    return data

def get_user(id=None):
    """Get a single user."""
    path = '/users/{id}'.format(id=id)
    data = git.request('GET', path)
    return data

def get_current_user():
    """Gets currently authenticated user."""
    path = '/user'
    data = git.request('GET', path)
    return data

def get_projects(**kwargs):
    """Get a list of projects accessible by the authenticated user."""
    path = '/projects'
    data = git.request('GET', path, **kwargs)
    return data

@app.route("/projects/owned", methods=["GET"])
def get_owned_projects(**kwargs):
    """Get a list of projects which are owned by the authenticated user."""
    path = '/projects/owned'
    data = git.request('GET', path, **kwargs)
    return data

@app.route("/projects/all", methods=["GET"])
def get_all_projects(**kwargs):
    """Get a list of all GitLab projects (admin only)."""
    path = '/projects/all'
    data = git.request('GET', path, **kwargs)
    return data

@namespace
def get_project(id=None):
    """Get a specific project which is owned by the authenticated user."""
    path = '/projects/{id}'.format(id=id)
    data = git.request('GET', path)
    return data

@namespace
def get_project_events(id=None):
    """Get the events for the specified project. Sorted from newest to
    latest."""
    path = '/projects/{id}/events'.format(id=id)
    data = git.request('GET', path)
    return data

@namespace
def get_project_team_members(id=None, **kwargs):
    """Get a list of a project's team members."""
    path = '/projects/{id}/members'.format(id=id)
    data = git.request('GET', path, **kwargs)
    return data

@namespace
def get_project_team_member(id=None, user_id=None):
    """Gets a project team member."""
    path = '/projects/{id}/members/{user_id}'.format(
        id=id, user_id=user_id
    )
    data = git.request('GET', path)
    return data

@namespace
def get_branches(id=None):
    """Lists all branches of a project."""
    path = '/projects/{id}/repository/branches'.format(id=id)
    data = git.request('GET', path)
    return data

@namespace
def get_branch(id=None, branch=None):
    """Lists a specific branch of a project."""
    path = '/projects/{id}/repository/branches/{branch}'.format(
        id=id, branch=branch
    )
    data = git.request('GET', path)
    return data

def get_commits(id=None, **kwargs):
    """Get a list of repository commits in a project."""
    path = '/projects/{id}/repository/commits'.format(id=id)
    data = git.request('GET', path)
    return data

def get_commit(id=None, sha=None):
    """Get a specific commit identified by the commit hash or name of a
    branch or tag."""
    path = '/projects/{id}/repository/commits/{sha}'.format(id=id, sha=sha)
    data = git.request('GET', path)
    return data

def get_commit_diff(self, id=None, sha=None):
    """Get the diff of a commit in a project."""
    path = '/projects/{id}/repository/commits/{sha}/diff'.format(
        id=id, sha=sha
    )
    data = self._request('GET', path)
    return data

def get_commit_comments(self, id=None, sha=None):
    """Get the comments of a commit in a project."""
    path = '/projects/{id}/repository/commits/{sha}/comments'.format(
        id=id, sha=sha
    )
    data = git.request('GET', path)
    return data

def get_merge_requests(id=None, **kwargs):
    """Get all merge requests for this project."""
    path = '/projects/{id}/merge_requests'.format(id=id)
    data = git.request('GET', path, **kwargs)
    return data

def get_merge_request(id=None, merge_request_id=None):
    """Shows information about a single merge request."""
    path = '/projects/{id}/merge_request/{merge_request_id}'.format(
        id=id, merge_request_id=merge_request_id
    )
    data = git.request('GET', path)
    return data

def get_merge_request_changes(id=None, merge_request_id=None):
    """Shows information about the merge request including its files and
    changes."""
    path = ('/projects/{id}/merge_request/{merge_request_id}/changes'
            ).format(id=id, merge_request_id=merge_request_id)
    data = git.request('GET', path)
    return data

def get_merge_request_comments(id=None, merge_request_id=None):
    """Gets all the comments associated with a merge request."""
    path = ('/projects/{id}/merge_request/{merge_request_id}/comments'
            ).format(id=id, merge_request_id=merge_request_id)
    data = git.request('GET', path)
    return data

def get_issues(**kwargs):
    """Get all issues created by authenticated user."""
    path = '/issues'
    data = git.request('GET', path, **kwargs)
    return data

def get_project_issues(id=None, **kwargs):
    """Get a list of project issues."""
    path = '/projects/{id}/issues'.format(id=id)
    data = git.request('GET', path, **kwargs)
    return data

def get_project_issue(id=None, issue_id=None):
    """Gets a single project issue."""
    path = '/projects/{id}/issues/{issue_id}'
    data = git.request('GET', path)
    return data


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
