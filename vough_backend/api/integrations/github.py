import requests
from django.conf import settings


class GithubApi:
    API_URL = settings.GITHUB_API_URL
    GITHUB_TOKEN = settings.GITHUB_TOKEN
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        r = requests.get(f'{GithubApi.API_URL}/orgs/{login}', headers=GithubApi.headers)
        return r.json()

    def get_organization_public_members(self, login: str):
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        r = requests.get(f'{GithubApi.API_URL}/orgs/{login}/public_members', headers=GithubApi.headers)
        return r.json()
