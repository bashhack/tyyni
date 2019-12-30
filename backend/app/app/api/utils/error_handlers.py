from pydantic.main import BaseModel


class ErrorMessage(BaseModel):
    message: str


class ResourceNotFoundException(Exception):
    def __init__(self, requested_id: int):
        self.requested_id = requested_id


class UserNotFoundException(ResourceNotFoundException):
    def __init__(self, user_id: int):
        self.user_id = user_id
        super(UserNotFoundException, self).__init__(requested_id=self.user_id)


class UserAlreadyExistsException(Exception):
    # TODO: Feeling uneasy about this whole approach - probably want to switch over
    #       to a 200_OK + notification email solution to avoid enumeration attacks
    #       For more, see: `create_user` in `app.api.api_v1.endpoints.users`
    def __init__(self, username: str):
        self.username = username
