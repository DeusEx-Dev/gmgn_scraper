from src.gmgn_scraper import GMGNScraper
from src.token_data_standardizer import TokenDataStandardizer
import asyncio
import json


def validate_address(address: str) -> bool:
    return len(address) >= 32 and len(address) <= 44


async def main():
    data_curator = TokenDataStandardizer()

    token_address = input('Insert a Solana token address: ').strip()
    if not validate_address(token_address):
        print('Error: Invalid token address format')
        return

    async with GMGNScraper() as scraper:
        try:
            print('Fetching token data...')
            token_data = await scraper.get_token_data(token_address)
            curated_data = data_curator.standardize(token_data)
        except Exception as e:
            print(f'Error fetching data: {str(e)}')
            return

    output_file = 'token_data.json'
    print(f'Saving results to {output_file}...')
    try:
        with open(output_file, 'w') as f:
            json.dump(curated_data, f, indent=2)
        print(f'Done! Check {output_file}')
    except IOError as e:
        print(f'Error saving file: {str(e)}')


if __name__ == '__main__':
    asyncio.run(main())
