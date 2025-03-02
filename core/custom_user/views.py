"""
This file is used to create the views for the custom user model.
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining a token pair.
    """

    def post(self, request, *args, **kwargs):
        """
        Post method for the view.

        Parameters
        ----------
        request : Request
            The request object.
        *args : list
            The arguments.
        **kwargs : dict
            The keyword arguments.

        Returns
        -------
        Response
            The response object.
        """

        response = super().post(request, *args, **kwargs)
        response.set_cookie(
            key="refresh_token",
            value=response.data.pop("refresh"),  # Remove from response, keep in cookie
            httponly=True,
            secure=True,  # Must be True to use SameSite=None
            samesite="None",  # Allow cross-site cookie usage
        )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing a token.
    """

    def post(self, request, *args, **kwargs):
        """
        Post method for the view.

        Parameters
        ----------
        request : Request
            The request object.
        *args : list
            The arguments.
        **kwargs : dict
            The keyword arguments.

        Returns
        -------
        Response
            The response object.
        """

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "No refresh token"}, status=400)

        request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)

        return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Return the currently authenticated user.

    Parameters
    ----------
    request : Request
        The request object.

    Returns
    -------
    Response
        The response object.
    """
    user = request.user

    return Response(UserSerializer(user).data)


class LogoutView(APIView):
    """
    View for logging out a user.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Post method for the view.

        Parameters
        ----------
        request : Request
            The request object.

        Returns
        -------
        Response
            The response object.
        """
        try:
            # Get refresh token from the HTTP-only cookie
            refresh_token = request.COOKIES.get("refresh_token")

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token

            # Create a response and delete the refresh_token cookie
            response = Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_205_RESET_CONTENT,
            )
            response.delete_cookie("refresh_token")

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
