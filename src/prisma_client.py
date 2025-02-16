""" Prisma Module

Exports `Prisma` client instance with db types and accessors.
"""
from prisma import (Prisma, register)

prisma = Prisma()

# Register the Prisma client so it can be used
register(prisma)