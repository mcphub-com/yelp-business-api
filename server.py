import requests
from datetime import datetime
from typing import Union, Literal, List
from mcp.server import FastMCP
from pydantic import Field
from typing import Annotated
from mcp.server.fastmcp import FastMCP
from fastmcp import FastMCP, Context
import os
from dotenv import load_dotenv
load_dotenv()
rapid_api_key = os.getenv("RAPID_API_KEY")
import logging
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__rapidapi_url__ = 'https://rapidapi.com/oneapiproject/api/yelp-business-api'

mcp = FastMCP('yelp-business-api')

@mcp.tool()
def search_yelp(location: Annotated[str, Field(description='Enter exact locations. For example, use Roosevelt, NY not Roosevelt only.')],
                search_term: Annotated[str, Field(description='Enter any search term you want, just like on Yelp. Ex. Coffee shop, Pizza shop, electrician, or plumber Ex. Black Owned Saloon, Mexican pizza shop')],
                limit: Annotated[Union[int, float, None], Field(description='Number of results per page. Max: 40 Default: 10. Default: 10')] = None,
                offset: Annotated[Union[int, float, None], Field(description='If offset is set to 0, it means start from zero. If offset is set to 20, it means to start showing after 20 results. Default: 0')] = None,
                business_details_type: Annotated[Literal['basic', 'advanced', None], Field(description="Basic: provides basic info's about the businesses. Advanced: provides in-depth information about the businesses (it's like using /search and /each business details endpoints at the same time) Advanced option costs 2 requests per call.")] = None) -> dict: 
    '''Use the same search box on yelp.com'''
    url = 'https://yelp-business-api.p.rapidapi.com/search'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'location': location,
        'search_term': search_term,
        'limit': limit,
        'offset': offset,
        'business_details_type': business_details_type,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def business_details(business_url: Annotated[Union[str, None], Field(description='Get the business details by Yelp Business URL.')] = None,
                     business_ids: Annotated[Union[str, None], Field(description='Get business details from business_id found from /search endpoint. Separate each using a comma. You can put up to 39 business ids on each request. Ex. BCUhfgjbVVvjs0ro4ATRsg,wj7ekipyvssV3Ok7p8zxGg, V2_qfjnwAVWqIphf7y866w')] = None) -> dict: 
    '''Scrape By Yelp URL: Ex. https://www.yelp.com/biz/capital-blossom-day-spa-washington or by business ids found from /search endpoint. You can get these business urls from the "/search" endpoint('YelpURL')'''
    url = 'https://yelp-business-api.p.rapidapi.com/each'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'business_url': business_url,
        'business_ids': business_ids,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def reviews(business_url: Annotated[Union[str, None], Field(description='Enter any business url from yelp.com (any subdomain)')] = None,
            business_id: Annotated[Union[str, None], Field(description='Enter any business ID found from /search endpoint')] = None,
            reviews_per_page: Annotated[Union[int, float, None], Field(description='Max value could be: 45 Default: 20')] = None,
            end_cursor: Annotated[Union[str, None], Field(description='For first page: Default is set to None For next pages, if hasNextPage = true : Input the end_cursor value found from the response of the previous page to get reviews of the next page. Ex. end_cursor = eyJ2ZXJzaW9uIjoxLCJ0eXBlIjoib2Zmc2V0Iiwib2Zmc2V0Ijo0NH0')] = None,
            sort_by: Annotated[Literal['Yelp_sort', 'Newest_first', 'Oldest_first', 'Highest_rated', 'Lowest_rated', 'Elites', None], Field(description='')] = None,
            rating_filter: Annotated[Literal['All_ratings', '5_stars', '4_stars', '3_stars', '2_stars', '1_star', None], Field(description='')] = None) -> dict: 
    '''Get business reviews by url or id'''
    url = 'https://yelp-business-api.p.rapidapi.com/reviews'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'business_url': business_url,
        'business_id': business_id,
        'reviews_per_page': reviews_per_page,
        'end_cursor': end_cursor,
        'sort_by': sort_by,
        'rating_filter': rating_filter,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def get_menus(business_id: Annotated[str, Field(description='Find restaurant menus if present on the Yelp website. Menus on personal websites cannot be collected.')]) -> dict: 
    '''Get restaurant menus if present on yelp'''
    url = 'https://yelp-business-api.p.rapidapi.com/get_menus'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'business_id': business_id,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def popular_dishes(business_id: Annotated[str, Field(description='Get popular dishes from a restaurant when available on the website. Input business_id.')]) -> dict: 
    '''Get popular_dish list of a restaurant when available on the website.'''
    url = 'https://yelp-business-api.p.rapidapi.com/popular_dish'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'business_id': business_id,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def business_url_to_id(business_url: Annotated[str, Field(description='Enter url to find the business id.')]) -> dict: 
    '''Find biz id from url.'''
    url = 'https://yelp-business-api.p.rapidapi.com/biz_url2id'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'business_url': business_url,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
def upcheck(check: Annotated[str, Field(description='')]) -> dict: 
    '''Check if the api status is live!'''
    url = 'https://yelp-business-api.p.rapidapi.com/upcheck'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}
    payload = {
        'check': check,
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    response = requests.get(url, headers=headers, params=payload)
    return response.json()

@mcp.tool()
async def get_full_yelp_list(
    location: Annotated[str, Field(description='Enter exact locations. For example, use Roosevelt, NY not Roosevelt only.')],
    search_term: Annotated[str, Field(description='Enter any search term you want, just like on Yelp. Ex. Coffee shop, Pizza shop, electrician, or plumber Ex. Black Owned Saloon, Mexican pizza shop')],
    start_page: Annotated[Union[int, None], Field(description='Start page number')] = None,
    end_page: Annotated[Union[int, None], Field(description='End page number (inclusive)')] = None,
    limit: Annotated[Union[int, float, None], Field(description='Number of results per page. Max: 40 Default: 10')] = None,
    business_details_type: Annotated[Literal['basic', 'advanced', None], Field(description="Basic: provides basic info's about the businesses. Advanced: provides in-depth information about the businesses (it's like using /search and /each business details endpoints at the same time) Advanced option costs 2 requests per call.")] = None
) -> dict:
    '''Search and return all results on yelp.com'''
    url = 'https://yelp-business-api.p.rapidapi.com/search'
    headers = {'x-rapidapi-host': 'yelp-business-api.p.rapidapi.com', 'x-rapidapi-key': rapid_api_key}

    # 校验 start_page 和 end_page 必须同时填写或都不填写
    if (start_page is None and end_page is not None) or (start_page is not None and end_page is None):
        raise ValueError("start_page 和 end_page must fill together，or not fill together")
    if start_page is None:
        start_page = 1
    if end_page is None:
        end_page = 8
    if limit is None:
        limit = 40

    import httpx, asyncio
    async def fetch_page(page):
        offset = (page - 1) * limit
        params = {
            'location': location,
            'search_term': search_term,
            'limit': limit,
            'offset': offset,
            'business_details_type': business_details_type,
        }
        params = {k: v for k, v in params.items() if v is not None}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, params=params)
            return resp.json()

    async def gather_all():
        tasks = [fetch_page(page) for page in range(start_page, end_page + 1)]
        results = await asyncio.gather(*tasks)
        all_businesses = []
        for result in results:
            if isinstance(result, dict):
                items = result.get('business_search_result', [])
                all_businesses.extend(items)
                logging.info(len(items))
        return {'all_businesses': all_businesses}

    return await gather_all()


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9997
    mcp.run(transport="stdio")
