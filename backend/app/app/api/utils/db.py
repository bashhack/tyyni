from app.db.session import Session


def get_db():
    """
    
    We need to have an independent database session/connection (Session) per request,
    then use the same session throughout the request lifecycle and, finally,
    close it after the request is finished.

    Technical details:

     - Only code prior to and including the yield statement is executed before sending a response.

     - The yielded value is what is injected into path operations and other dependencies.
    
     - The code following the yield statement is executed after the response has been delivered.
    """

    db = Session()
    try:
        yield db
    finally:
        db.close()
