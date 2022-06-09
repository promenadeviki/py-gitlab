# -*- coding: utf-8 -*-
import http.client as httplib # Httplib was changed to http.client in python3
import requests
import os
from decouple import config
from decorators import namespace
from exceptions import GitLabServerError


class GitLab(object):
    # Use v4 gitlab api version. Others are deprecated in Python
    Version = 'v4'
    ResponseError = GitLabServerError

    def __init__(self, host=None, private_token=None, use_ssl=True):
        '''
        Uses decouple to parse .env file and also sets gitlab.com host
        '''
        self.host = host
        self.use_ssl = use_ssl
        private_token = config('TOKEN')
        self._set_headers(private_token)

    @property
    def _base_url(self):
        """Set the GitLab API base URL."""
        protocol = 'https' if self.use_ssl else 'http'
        base_url = '{protocol}://{host}/api/{version}'.format(
            protocol=protocol, host=self.host, version=self.Version
        )
        return base_url

    def _set_headers(self, private_token):
        """Set `PRIVATE_TOKEN` HTTP request header for restricted endpoints."""
        self._session = requests.Session()
        # Set HTTP `Authorization` request header for the `Session` object
        self._session.headers.update({
            'PRIVATE-TOKEN': '{private_token}'.format(
                private_token=private_token
            )
        })

    def get_users(self, **kwargs):
        """Get a list of users."""
        path = '/users'
        data = self._request('GET', path, **kwargs)
        return data

    def get_user(self, id=None):
        """Get a single user."""
        path = '/users/{id}'.format(id=id)
        data = self._request('GET', path)
        return data

    def get_current_user(self):
        """Gets currently authenticated user."""
        path = '/user'
        data = self._request('GET', path)
        return data

    def get_projects(self, **kwargs):
        """Get a list of projects accessible by the authenticated user."""
        path = '/projects'
        data = self._request('GET', path, **kwargs)
        return data

    def get_owned_projects(self, **kwargs):
        """Get a list of projects which are owned by the authenticated user."""
        path = '/projects/owned'
        data = self._request('GET', path, **kwargs)
        return data

    def get_all_projects(self, **kwargs):
        """Get a list of all GitLab projects (admin only)."""
        path = '/projects/all'
        data = self._request('GET', path, **kwargs)
        return data

    @namespace
    def get_project(self, id=None):
        """Get a specific project which is owned by the authenticated user."""
        path = '/projects/{id}'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_project_events(self, id=None):
        """Get the events for the specified project. Sorted from newest to
        latest."""
        path = '/projects/{id}/events'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_project_team_members(self, id=None, **kwargs):
        """Get a list of a project's team members."""
        path = '/projects/{id}/members'.format(id=id)
        data = self._request('GET', path, **kwargs)
        return data

    @namespace
    def get_project_team_member(self, id=None, user_id=None):
        """Gets a project team member."""
        path = '/projects/{id}/members/{user_id}'.format(
            id=id, user_id=user_id
        )
        data = self._request('GET', path)
        return data

    @namespace
    def get_branches(self, id=None):
        """Lists all branches of a project."""
        path = '/projects/{id}/repository/branches'.format(id=id)
        data = self._request('GET', path)
        return data

    @namespace
    def get_branch(self, id=None, branch=None):
        """Lists a specific branch of a project."""
        path = '/projects/{id}/repository/branches/{branch}'.format(
            id=id, branch=branch
        )
        data = self._request('GET', path)
        return data

    def get_commits(self, id=None, **kwargs):
        """Get a list of repository commits in a project."""
        path = '/projects/{id}/repository/commits'.format(id=id)
        data = self._request('GET', path)
        return data

    def get_commit(self, id=None, sha=None):
        """Get a specific commit identified by the commit hash or name of a
        branch or tag."""
        path = '/projects/{id}/repository/commits/{sha}'.format(id=id, sha=sha)
        data = self._request('GET', path)
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
        data = self._request('GET', path)
        return data

    def get_merge_requests(self, id=None, **kwargs):
        """Get all merge requests for this project."""
        path = '/projects/{id}/merge_requests'.format(id=id)
        data = self._request('GET', path, **kwargs)
        return data

    def get_merge_request(self, id=None, merge_request_id=None):
        """Shows information about a single merge request."""
        path = '/projects/{id}/merge_request/{merge_request_id}'.format(
            id=id, merge_request_id=merge_request_id
        )
        data = self._request('GET', path)
        return data

    def get_merge_request_changes(self, id=None, merge_request_id=None):
        """Shows information about the merge request including its files and
        changes."""
        path = ('/projects/{id}/merge_request/{merge_request_id}/changes'
                ).format(id=id, merge_request_id=merge_request_id)
        data = self._request('GET', path)
        return data

    def get_merge_request_comments(self, id=None, merge_request_id=None):
        """Gets all the comments associated with a merge request."""
        path = ('/projects/{id}/merge_request/{merge_request_id}/comments'
                ).format(id=id, merge_request_id=merge_request_id)
        data = self._request('GET', path)
        return data

    def get_issues(self, **kwargs):
        """Get all issues created by authenticated user."""
        path = '/issues'
        data = self._request('GET', path, **kwargs)
        return data

    def get_project_issues(self, id=None, **kwargs):
        """Get a list of project issues."""
        path = '/projects/{id}/issues'.format(id=id)
        data = self._request('GET', path, **kwargs)
        return data

    def get_project_issue(self, id=None, issue_id=None):
        """Gets a single project issue."""
        path = '/projects/{id}/issues/{issue_id}'
        data = self._request('GET', path)
        return data

    def _request(self, method, url, data={}, **kwargs):
        """Wrapper method for making requests to endpoints."""
        url = self._base_url + url
        res = self._session.request(method, url, params=kwargs, data=data)
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

    def __str__(self):
        return '{}:{}'.format(self.__class__.__name__, self.host)

    def __repr__(self):
        return self.__str__()
