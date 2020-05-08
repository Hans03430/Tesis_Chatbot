import asyncio
from aiofile import AIOFile
from aiohttp import ClientSession
from bs4 import BeautifulSoup

async def get_webpage_as_bs(session: ClientSession, url: str) -> BeautifulSoup:
    """
    Obtains an html webapge as a BeautifulSoup object

    This function converts a static webpage into a beautiful Soup object, for ease of
    ineraction with python. It requires the url to find the webpage and convert it.

    Parameters:
    session (ClientSession): The async session used to obtain the webpage
    url (str): The url of the webpage to convert

    Returns:
    BeautifulSoup: The BeautifulSoup object that represents the webpage found by the url
    """
    try:
        webpage = await session.get(url)
        html_text = await webpage.read()
        return BeautifulSoup(html_text, 'html.parser')
    except Exception as e:
        raise e


async def download_document_and_save(session: ClientSession, url: str, dir: str) -> None:
    """
    This function downloads a document from a given link.

    This function uses asyncronous calls to obtain a downloadable object from a link and
    saves it at a certain location in the current computer

    Parameters:
    session (ClientSession): The async session used to obtain the webpage
    url (str): The url of the webpage to convert
    dir (str): The directory where to save this document

    Returns:
    None
    """
    async with session.get(url) as response:
        try:
            if response.status == 200: # Document still exists
                document = await response.read()
                async with AIOFile(dir, 'wb') as downloaded_file:
                    await downloaded_file.write(document)
        except Exception as e:
            raise e
