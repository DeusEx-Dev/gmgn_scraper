import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TokenDataStandardizer:
    def standardize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to standardize token data"""
        try:
            token_info = self._extract_token_info(raw_data)
            rug_vote = self._extract_rug_vote(raw_data)
            security = self._extract_security_analysis(raw_data)
            holders = self._extract_holders_info(raw_data)
            wallets = self._extract_wallets_data(raw_data)
            top_holders = self._extract_top_holders_data(raw_data)

            return {
                'token_info': token_info,
                'rug_vote': rug_vote,
                'security_analysis': security,
                'holders_info': holders,
                'wallets_data': wallets,
                'top_holders': top_holders,
            }
        except Exception as e:
            logger.error(f'Error standardizing token data: {str(e)}')
            raise

    def _extract_token_info(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and structure token information"""
        try:
            token_data = raw_data['mutil_window_token_info']['data'][0]

            return {
                'name': token_data['name'],
                'symbol': token_data['symbol'],
                'contract_address': token_data['address'],
                'total_supply': token_data['total_supply'],
                'price': token_data['price']['price'],
                'holder_count': token_data['holder_count'],
                'volume': {
                    'volume_1h': token_data['price']['volume_1h'],
                    'volume_1m': token_data['price']['volume_1m'],
                    'volume_24h': token_data['price']['volume_24h'],
                    'volume_5m': token_data['price']['volume_5m'],
                    'volume_6h': token_data['price']['volume_6h'],
                },
                'dev': token_data['dev'],
                'open_timestamp': token_data['open_timestamp'],
                'creation_timestamp': token_data['creation_timestamp'],
            }
        except KeyError as e:
            logger.error(f'Missing key in token info data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting token info: {str(e)}')
            raise

    def _extract_rug_vote(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract rug and social information"""
        try:
            rug_data = raw_data['mutil_window_token_link_rug_vote']['data']

            return {'socials': rug_data['link'], 'rug': rug_data['rug']}
        except KeyError as e:
            logger.error(f'Missing key in rug vote data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting rug vote info: {str(e)}')
            raise

    def _extract_security_analysis(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract security analysis data"""
        try:
            return raw_data['mutil_window_token_security_launchpad']['data']['security']
        except KeyError as e:
            logger.error(f'Missing key in security data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting security analysis: {str(e)}')
            raise

    def _extract_holders_info(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract holder statistics"""
        try:
            return raw_data['token_holder_stat']['data']
        except KeyError as e:
            logger.error(f'Missing key in holder data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting holder info: {str(e)}')
            raise

    def _extract_wallets_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract wallet statistics"""
        try:
            return raw_data['token_wallet_tags_stat']['data']
        except KeyError as e:
            logger.error(f'Missing key in wallet data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting wallet data: {str(e)}')
            raise

    def _extract_top_holders_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract top holder wallets data"""
        try:
            return raw_data['top_holders']['data']
        except KeyError as e:
            logger.error(f'Missing key in wallet data: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'Error extracting wallet data: {str(e)}')
            raise
