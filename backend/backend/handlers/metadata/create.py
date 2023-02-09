import json
import traceback

from backend.handlers.metadata import logger, mask_sensitive_data, build_response, create_or_update, validate_event, validate_body, ValidationError


def lambda_handler(event, context):
    logger.info(mask_sensitive_data(event))
    try:

        validate_event(event)
        
        body = validate_body(event)
        assetId = event['pathParameters']['assetId']

        create_or_update(assetId, body['metadata'])

        return build_response(200, json.dumps({ "status": "OK" }))
    except ValidationError as ex:
        logger.info(traceback.format_exc())
        return build_response(ex.code, json.dumps(ex.resp))
    except Exception as ex:
        logger.error(traceback.format_exc())
        return build_response(500, "Server Error")