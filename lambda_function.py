import json

from geosprite.eo.catalog.stac import Catalog
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event,context):
    logger.info(event)
    logger.info(context)

    # 提取 queryStringParameters 中的值
    requests = json.loads(event['body'])
    start_date = requests['start_date']
    end_date = requests['end_date']
    bbox = requests['bbox']
    cloud_cover = requests['cloud_cover']

    # 使用aws的sentinel2测试
    stac_api = 'https://earth-search.aws.element84.com/v1'
    collection_id = 'sentinel-2-l2a'

    # 调用 Catalog.search() 方法进行搜索
    catalog = Catalog(stac_api)
    try:
        results = catalog.search(collection_id, start_date=start_date, end_date=end_date, cloud_cover=cloud_cover, bbox=bbox)
        results_list=[]
        for result in results:
            results_list.append(result.to_dict())

        logger.info(f"From {stac_api}, {collection_id}, found {len(results_list)} result.")

        # 构建完整的响应对象
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(results_list)
        }

        return response
    except Exception as e:
        logger.error(e)
        response = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': {"error": e}
        }

        return response


