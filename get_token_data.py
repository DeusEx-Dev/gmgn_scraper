from src.gmgn_scraper import GMGNScraper
from src.token_data_standardizer import TokenDataStandardizer
import asyncio
import json


async def main():
    data_curator = TokenDataStandardizer()

    print('Fetching token addresses...')
    token_address = input('Insert a Solana token address: ')

    async with GMGNScraper() as scraper:
        try:
            token_data = await scraper.get_token_data(token_address)
            curated_data = data_curator.standardize(token_data)
        except Exception as e:
            print(f'Unexpected error: {str(e)}')
            return

    print('Saving results...')
    with open('token_data.json', 'w') as f:
        json.dump(curated_data, f, indent=2)
    print('Done! Check token_data_list.json')


if __name__ == '__main__':
    asyncio.run(main())
