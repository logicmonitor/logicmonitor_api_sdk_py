# coding: utf-8


class ResonseInterface(object):
  """
  This is the callback interface for handling the response.
  End user can create his own class using this one to get the response status.
  """

  def __init__(self):
    super(ResonseInterface, self).__init__()

  @classmethod
  def success_callback(self, request, response, status, request_id):
    """
    This callback gets invoked for successful response from the end REST endpoint.

    Args:
        request (:obj:`dict` of :obj:`str`): The json payload send to REST endpoint.
        response (:obj:`dict` of :obj:`str`): Response received from the REST endpoint.
        status (:obj:`int`): HTTP status code.
        request_id (:obj:`str`): Unique request id generated by Rest endpoint.
    """
    pass

  @classmethod
  def error_callback(self, request, response, status, request_id, reason):
    """
    This callback gets invoked for any error or exception from the end REST endpoint.

    Args:
        request (:obj:`dict` of :obj:`str`): The json payload send to REST endpoint.
        response (:obj:`dict` of :obj:`str`): Response received from the REST endpoint.
        status (:obj:`int`): HTTP status code.
        request_id (:obj:`str`): Unique request id generated by Rest endpoint.
        reason (:obj:`str`): The reason for error.
    """
    pass