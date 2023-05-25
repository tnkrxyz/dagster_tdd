from dagster import op, get_dagster_logger
import pandas as pd

logger = get_dagster_logger()

@op
def fields_exist(asset:pd.DataFrame, args: list):
	if not set(args).issubset(asset.columns):
		return False
	return True

@op
def field_ge_0(asset: pd.DataFrame, args: str):
  return (asset[args] >= 0).all()

@op
def field_lt_0(asset: pd.DataFrame, args: str):
  return (asset[args] < 0).all()

@op
def tvl_is_positive(context, asset: pd.DataFrame):
	status = field_ge_0(asset, 'tvl')
	if status:
		context.log.info("tvl_is_positive check passed")
	else:
		context.log.error("tvl_is_positive check failed")
	return status

@op
def tvl_is_negative(context, asset: pd.DataFrame):
	status = field_lt_0(asset, 'tvl')
	if status:
		context.log.info("tvl_is_negative check passed")
	else:
		context.log.error("tvl_is_negative check failed")
	return status

@op
def check_amount_is_positive(context, asset: pd.DataFrame):
	status = field_ge_0(asset, 'amount')
	if status:
		context.log.info("check_amount_is_positive check passed")
	else:
		context.log.error("check_amount_is_positive check failed")
	return status

@op
def check_protocol_fields(context, asset: pd.DataFrame):
	status = fields_exist(asset, ['slug', 'type'])
	if status:
		context.log.info("check_protocol_fields check passed")
	else:
		context.log.error("check_protocol_fields check failed")
	return status

@op
def check_dex_pool_fields(context, asset: pd.DataFrame):
	status =  fields_exist(asset, ['id', 'symbol'])
	if status:
		context.log.info("check_dex_pool_fields check passed")
	else:
		context.log.error("check_dex_pool_fields check failed")
	return status

@op
def check_lending_market_fields(context, asset: pd.DataFrame):
	status =  fields_exist(asset, ['id', 'name'])
	if status:
		context.log.info("check_lending_market_fields check passed")
	else:
		context.log.error("check_lending_market_fields check failed")
	return status