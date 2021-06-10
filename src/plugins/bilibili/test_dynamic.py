import pytest

from .dynamic.datasource import getDynamicStatus


@pytest.mark.asyncio
async def test():
    a = await getDynamicStatus(uid='2', debug=1)
    print(a)
