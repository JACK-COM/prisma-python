"""
User-related prisma models. Can be used to define custom selection fields for 
`prisma` client instance. This prevents you from having to delete fields from
large lists of records before returning them as an API response.
"""
from prisma.bases import BaseUser


class SafeUser(BaseUser):
    """
    A Prisma `User` model that only exposes name, email, and username.

    Demonstrates how you can select fields in `Prisma`, as a workaround for
    the missing `select: { /* ...user fields... */ }` query option.)
    """

    email: str
    username: str
    firstName: str
    lastName: str
