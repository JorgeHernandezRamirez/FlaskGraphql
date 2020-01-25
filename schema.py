import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import UserModel


class AndSQLAlchemyConnectionField(SQLAlchemyConnectionField):
    def get_args(self, **args):
        fields_to_remove = ['first', 'last', 'before', 'after']
        return {key: value for key, value in args.items() if key not in fields_to_remove}

    def add_filter_to_query(self, model, query, filters: dict):
        for key in filters.keys():
            query = query.filter(getattr(model, key) == filters[key])
        return query

    @classmethod
    def get_query(cls, model, info, sort=None, **args):
        query_to_return = super().get_query(model, info, sort=None, **args)
        query_to_return = cls.add_filter_to_query(cls, model, query_to_return, cls.get_args(cls, **args))
        return query_to_return


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    # user = graphene.List(lambda: User, name=graphene.String())
    user = AndSQLAlchemyConnectionField(User, name=graphene.String()) #Esto se puede meter dentro del __init__ para que contemple todos los campos

    """def resolve_user(self, info, **kwargs):
        query = User.get_query(info)
        if len(kwargs) == 0:
            return query.all()
        return query.filter(UserModel.name == kwargs.get('name')).all()"""


schema = graphene.Schema(query=Query, types=[User])
