import sys

sys.path.extend('../../src')

import requests
from aiohttp import ClientSession
import asyncio
import time
from src.data_obtaining.webpage_interaction import get_webpage_as_bs

async def obtener_propuestas_laborales(session: ClientSession, url: str) -> None:
        # page = requests.get(url)
        """page = await session.get(url)
        page_content = await page.read()
        soup = BeautifulSoup(page_content, 'html.parser')"""
        soup = await get_webpage_as_bs(session, url)
        results = soup.find(id='ResultsContainer')
        job_elems = results.find_all('section', class_='card-content')

        for job_elem in job_elems:
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('div', class_='company')
            location_elem = job_elem.find('div', class_='location')
            if None in (title_elem, company_elem, location_elem):
                continue
            print(title_elem.text.strip())
            print(company_elem.text.strip())
            print(location_elem.text.strip())
            print()

        python_jobs = results.find_all('h2', string=lambda text: 'python' in text.lower())
        for p_job in python_jobs:
            link = p_job.find('a')['href']
            print(p_job.text.strip())
            print(f'Apply here: {link}\n')

    
URLS = ['https://www.monster.com/jobs/search/?q=Software-Developer&where=Australia',
        'https://www.monster.com/jobs/search/?q=Software-Developer&where=Germany'
        'https://www.monster.com/jobs/search/?q=Software-Developer&where=France'
        'https://www.monster.com/jobs/search/?q=Software-Developer&where=Peru'
        'https://www.monster.com/jobs/search/?q=Software-Developer&where=Russia']


async def main() -> None:
    session = ClientSession()
    start = time.time()
    for url in URLS:
        await obtener_propuestas_laborales(session, url)

    print(f'Tiempo de ejecución {time.time() - start}s')
    """content = await session.get('http://www.perueduca.pe/recursosedu/textos-del-med/inicial/comunicacion/momentos-de-cuidado-2.pdf')
    text = await content.read()
    open('coso.pdf', 'wb').write(text)"""
    await session.close()

if __name__ == "__main__":
    asyncio.run(main())