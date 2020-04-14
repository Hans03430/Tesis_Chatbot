import asyncio
import os
import pprint
import sys
sys.path.extend('../../src')

from aiohttp import ClientSession
from bs4 import Comment
from src.data_obtaining.webpage_interaction import get_webpage_as_bs, download_document_and_save

URLS = ['http://www.perueduca.pe/materiales-educativos?p_p_id=ResourcesPublicPE_WAR_ResourcesPublicPEportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_jspPage=%2Farea.jsp&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_areaId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_gradoId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_inicio=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_fin=10&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_tiporec=20',
        'http://www.perueduca.pe/materiales-educativos?p_p_id=ResourcesPublicPE_WAR_ResourcesPublicPEportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_jspPage=%2Farea.jsp&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_areaId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_gradoId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_inicio=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_fin=10&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_tiporec=17',
        'http://www.perueduca.pe/materiales-educativos?p_p_id=ResourcesPublicPE_WAR_ResourcesPublicPEportlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&p_p_col_id=column-1&p_p_col_count=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_jspPage=%2Farea.jsp&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_areaId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_gradoId=&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_inicio=1&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_fin=10&_ResourcesPublicPE_WAR_ResourcesPublicPEportlet_tiporec=18']

LEVELS = {
    'Educación Inicial': '1',
    'Educación Primaria': '2',
    'Educación Secundaria': '3'
}

ACCEPTED_LANGUAGE = 'ES (Español)'

async def obtain_and_save_document(session: ClientSession, url: str) -> None:
    """
    This function looks for the link to download a document in "perueduca.com"

    Parameters:
    session (ClientSession): The async session used to obtain the webpage
    url (str): The url of the webpage to convert

    Returns:
    None
    """
    soup = await get_webpage_as_bs(session, url)
    document_information_table = soup.find('div', id='ficha-catalogo').find_all('tr')
    document_language = document_information_table[7].find('td').text.strip()
    if (document_language == ACCEPTED_LANGUAGE):
        document_level = LEVELS[document_information_table[1].find('td').text.strip()]
        download_link = soup.find('a', id='hf_iframe')['href']
        document_name = download_link.split('/')[-1]
        storage_directory = os.getcwd() + f'/data/raw/pdf/{document_level}/{document_name}'
        print(storage_directory)
        await download_document_and_save(session, download_link, storage_directory)
        print(f'Document {document_name} downloaded successfully')

async def obtain_texts_from_perueduca_webpage(session: ClientSession, url: str) -> None:
    """
    This function traverses through an entire web page of peru educa, searching for documents to download.
    It's a recursive function.
    
    This function begins with obtaining the webpage as a beautiful soup object, then, it proceeds to find
    all the available document sections in this page so it can download them. After that, it goes to the
    next page and does the same process again.

    Parameters:
    session (ClientSession): The async session used to obtain the webpage
    url (str): The url of the webpage to convert

    Returns:
    None
    """
    soup = await get_webpage_as_bs(session, url)
    texts_information = soup.find_all('div', class_='box-result')
    if (len(texts_information) == 0): # No more texts in this page. Extraction process finished
        return
    else: # More texts still available
        for text in texts_information:
            text_link = text.find('a')['href']
            await obtain_and_save_document(session, text_link)
        # There are still more pages to look documents into
        next_page_button = soup.find('li', class_='next')
        next_page_url = next_page_button.find('a')['href']
        await obtain_texts_from_perueduca_webpage(session, next_page_url)


async def main():
    session = ClientSession()
    for url in URLS:
        await obtain_texts_from_perueduca_webpage(session, url)
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())