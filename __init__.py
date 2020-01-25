from flask_graphql import GraphQLView

from app import app
from schema import schema

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)


@app.route('/')
def index():
    return '<p> Hello World</p>'


if __name__ == '__main__':
    app.run()
