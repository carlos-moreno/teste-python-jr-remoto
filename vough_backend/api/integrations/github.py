import requests
from django.conf import settings


class GithubApi:
    API_URL = settings.GITHUB_API_URL
    GITHUB_TOKEN = settings.GITHUB_TOKEN
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}

    def get_organization(self, login: str):
        """Busca uma organização no Github

        :login: login da organização no Github
        """
        r = requests.get(f"{GithubApi.API_URL}/orgs/{login}", headers=GithubApi.headers)
        return r.json()

    def get_organization_qtd_public_members(self, login: str) -> int:
        """Retorna todos os membros públicos de uma organização

        :login: login da organização no Github
        """
        r = requests.get(
            f"{GithubApi.API_URL}/orgs/{login}/public_members",
            headers=GithubApi.headers,
        )
        return len(r.json())

    def get_organization_qtd_public_repo(self, login: str) -> int:
        return self.get_organization(login)["public_repos"]

    def get_organization_score(self, login: str) -> int:
        return self.get_organization_qtd_public_members(login) \
               + self.get_organization_qtd_public_repo(login)
