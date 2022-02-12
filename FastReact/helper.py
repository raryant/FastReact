import aiofiles
async def read_file(file_name):
    async with aiofiles.open(file_name, mode='r') as f:
        return await f.read()