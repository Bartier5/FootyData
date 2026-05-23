import aiohttp
import asyncio
import time
from config import get_headers,URLS, REQUEST_TIMEOUT,MAX_RETRIES, DELAY_BETWEEN
from utils import logger, log_call

async def fetch_page(session: aiohttp.ClientSession, url: str, league:str ):
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Fetching {league} | attempt {attempt}")
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)) as response:
                response.raise_for_status()
                html = await response.text()
                logger.info(f"✓ Got {league} | {len(html)} chars")
                return {"league": league, "html": html}
        except aiohttp.ClientResponseError as e:
               logger.error(f"HTTP error on {league}: {e.status}")
        except asyncio.TimeoutError:
            logger.error(f"Timeout on {league} | attempt {attempt}")
        except Exception as e:
            logger.error(f"Unexpected error on {league}: {e}")
        if attempt < MAX_RETRIES:
            logger.info(f"Retrying in {DELAY_BETWEEN}s...")
            await asyncio.sleep(DELAY_BETWEEN)

    logger.error(f"✗ All retries failed for {league}")
    return None
@log_call
def scrape_all():
    async def _run():
        async with aiohttp.ClientSession(headers=get_headers()) as session:
            tasks = []
            for league in URLS:
                u = URLS[league]
                tasks.append(fetch_page(session, u, league))
            responses = await asyncio.gather(*tasks)
            return [r for r in responses if r is not None]
    return asyncio.run(_run())