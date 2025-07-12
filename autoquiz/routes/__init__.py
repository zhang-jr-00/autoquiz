from flask_restx import Api

def register_routes(app):
    """Register all API routes"""
    # Initialize Flask-RESTx
    api = Api(
        app,
        version='1.0',
        title='Quiz Generator API',
        description='API for generating quizzes from input text or uploaded PDFs',
        doc='/api/docs'
    )
    
    # Import namespaces
    from autoquiz.routes.documents import ns as documents_ns
    from autoquiz.routes.quiz import ns as quiz_ns
    
    # Add namespaces to the API
    api.add_namespace(documents_ns)
    api.add_namespace(quiz_ns)
    
    return api