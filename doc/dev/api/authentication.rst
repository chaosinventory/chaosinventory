.. _`api_authentication`:


Authentication
==============

In order to use the API you need to authenticate yourself. In future there
will be multiple ways to do use, currently the only option is via an token.

Token Authentication
--------------------

Obtaining a token is possible via two ways:

* If you're not authenticated
    Send an POST request with a body containing the following attributes to
    ``/api/authentication/token/credentials``

    ============= ========== ========== ===================== =============================================================================
     Attribute    Required   Default           Type                                           Description
    ============= ========== ========== ===================== =============================================================================
    username      yes                   string
    password      yes                   string
    application   yes                   string                Application requesting the Authentication token (only for user information)
    expiring      no         infinite   DateTime (iso-8601)   Date and time when the token expires
    renewable     no         true       boolean               Whether the token is renewable
    ============= ========== ========== ===================== =============================================================================

    The following body is an example with only the required attributes given

    .. code-block:: json

        {
            "username": "test",
            "password": "foobar",
            "application": "Web"
        }

    You will receive a json response that looks like the following example

    .. code-block:: json

        {
            "token": "fce7780c725443ce86d89035a3680ebf0a56f4744b47b7c1307b89fc94e00f16"
        }

* If you're authenticated
    Send an POST request with a body containing the following attributes to
    ``/api/authentication/token``

    ============= ========== ========== ===================== =============================================================================
     Attribute     Required   Default           Type                                           Description
    ============= ========== ========== ===================== =============================================================================
    application   yes                   string                Application requesting the Authentication token (only for user information)
    expiring      no         infinite   DateTime (iso-8601)   Date and time when the token expires
    renewable     no         true       boolean               Whether the token is renewable
    ============= ========== ========== ===================== =============================================================================

    You will receive a json response that looks like the following example

    .. code-block:: json

        {
            "token": "fce7780c725443ce86d89035a3680ebf0a56f4744b47b7c1307b89fc94e00f16"
        }

This token can be used in an ``Authorization`` Header like this:
::
    Authorization: Token fce7780c725443ce86d89035a3680ebf0a56f4744b47b7c1307b89fc94e00f16

You're successfully authenticated :)

There are other API methods that have something to do with authentication tokens:

* List tokens (GET ``/api/authentication/token``)
    This API endpoint list all authentication tokens of the user logged in.

    Response format:
    List of objects with the following attributes:

   ================= ============================= ====================================================================================== ========================================
       Attribute                 Type                                                   Description                                                       Example
   ================= ============================= ====================================================================================== ========================================
    id                string                        The UUID identifying the token (not used for authentication)                           "6e3e9493-e458-462e-a31e-b0de8ea3ca83"
    token_beginning   string                        The first 6 characters of the token                                                    "fce778"
    application       string                        The application which created the token                                                "Web"
    created           DateTime (iso-8601)           The date when the token was created                                                    "2021-04-23T14:29:53.087016Z"
    expiring          null or DateTime (iso-8601)   Date and time when the token expires (may be ``null`` when the token doesn't expire)   "2021-04-24T14:29:53.087016Z"
    renewable         boolean                       Is the token renewable?                                                                true
   ================= ============================= ====================================================================================== ========================================


* Renew the token (POST ``/api/authentication/token/renew``)
    This API endpoint renews the authentication token the user authenticated
    with. This only works, when the token is renewable. In this process the
    old token is invalidated and a new token is created with the given options
    and the application from the old token.

    Request format:

    ============= ========== ========== ===================== =============================================================================
     Attribute     Required   Default           Type                                           Description
    ============= ========== ========== ===================== =============================================================================
    expiring      no         infinite   DateTime (iso-8601)   Date and time when the token expires
    renewable     no         true       boolean               Whether the token is renewable
    ============= ========== ========== ===================== =============================================================================

    Response:

    .. code-block:: json

        {
            "token": "fce7780c725443ce86d89035a3680ebf0a56f4744b47b7c1307b89fc94e00f16"
        }

* Revoke a token (POST ``/api/authentication/token/${id}``)
    With this API endpoint a token can be revoked. The UUID of the token must be passed as URI parameter.

    When successful the endpoint responds with ``"OK"``.
