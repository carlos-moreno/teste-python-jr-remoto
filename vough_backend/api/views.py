from rest_framework import viewsets, status
from rest_framework.views import Response

from api import models, serializers
from api.integrations.github import GithubApi

from django.shortcuts import get_object_or_404

# TODOS:
# 1 - Buscar organização pelo login através da API do Github
# 2 - Armazenar os dados atualizados da organização no banco
# 3 - Retornar corretamente os dados da organização
# 4 - Retornar os dados de organizações ordenados pelo score na listagem da API


class OrganizationViewSet(viewsets.ModelViewSet):

    queryset = models.Organization.objects.all()
    serializer_class = serializers.OrganizationSerializer
    lookup_field = "login"

    def retrieve(self, request, login=None):
        api_gh = GithubApi()
        resp = api_gh.get_organization(login)
        try:
            organization = models.Organization(
                login=login,
                name=resp["name"],
                score=api_gh.get_organization_score(login),
            )
            organization.save()
            serializer = serializers.OrganizationSerializer(organization)
            response = Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            response = Response(status=status.HTTP_404_NOT_FOUND)
        return response

    def list(self, request, login=None):
        queryset = models.Organization.objects.all()
        serializer = serializers.OrganizationSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, login):
        organization = get_object_or_404(models.Organization, login=login)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
