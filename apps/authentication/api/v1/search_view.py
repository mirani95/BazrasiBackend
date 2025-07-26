# from apps.authentication.api.v1.serializers.serializer import UserSerializer
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.viewsets import ModelViewSet, ViewSet
# from apps.authentication.document import UserDocument
# from rest_framework.response import Response
# from django.http.response import HttpResponse
# from apps.authentication.models import User
# from rest_framework.views import APIView
# from elasticsearch_dsl.query import Q
# import abc
#
#
# class PaginatedElasticSearchApiView(APIView, LimitOffsetPagination):
#     """Base ApiView Class for elasticsearch views with pagination,
#     Other ApiView classes should inherit from this class"""
#     serializer_class = None
#     document_class = None
#
#     @abc.abstractmethod
#     def generate_q_expression(self, query):
#         """This method should be overridden
#         and return a Q() expression."""
#
#     def get(self, request, query):
#         try:
#             q = self.generate_q_expression(query)
#             search = self.document_class.search().query(q)
#             response = search.execute()
#
#             print(f"Found {response.hits.total.value} hit(s) for query: '{query}'")
#
#             results = self.paginate_queryset(response, request, view=self)  # noqa
#             serializer = self.serializer_class(results, many=True)
#             return self.get_paginated_response(serializer.data)
#         except Exception as e:
#             return HttpResponse(e, status=500)
#
#
# class SearchUsersApiView(PaginatedElasticSearchApiView):  # noqa
#     """Search in Users"""
#
#     serializer_class = UserSerializer
#     document_class = UserDocument
#
#     def generate_q_expression(self, query):
#         return Q(
#             'multi_match',
#             query=query,
#             fields=[
#                 'username',
#                 'mobile'
#             ], fuzziness='auto'
#         )
