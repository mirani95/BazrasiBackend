# from .models import User, Province
# from django_elasticsearch_dsl import Document, fields
# from django_elasticsearch_dsl.registries import registry
#
#
# @registry.register_document
# class UserDocument(Document):
#     """ElasticSearch Document for indexing users"""
#
#     class Index:
#         name = 'users'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 0  # number of copies from data in document
#         }
#
#     class Django:
#         model = User
#         fields = [
#             "id",
#             "username",
#             "mobile",
#             "nationality"
#         ]
