from dagster import AssetKey, Definitions, SourceAsset, asset, job, get_dagster_logger
import pandas as pd
from .rule_def import rules

logger = get_dagster_logger()

def asset_factory(subgraph: dict[str, str]):
    # need to do this because group_name cannot have "-"
    slug_ = subgraph["slug"].replace("-", "_") 
    assets = []
    @asset(group_name=slug_, key_prefix=slug_)
    def protocol(context):
        #use subgraph slug to fetch protocol
        return pd.DataFrame({'slug': [subgraph["slug"]], 'type': subgraph["type"], 'tvl': 1000000})
    
    assets.append(protocol)
    if subgraph["type"] == "dex":
        @asset(group_name=slug_, key_prefix=slug_)
        def pool(context):
            #use subgraph slug to fetch pools
            return pd.DataFrame({'id': ['0x00'], 'symbol': "WETH/USDC"})
    
        @asset(group_name=slug_, key_prefix=slug_)
        def swap(context):
            #use subgraph slug to fetch pools
            return pd.DataFrame({'id': ['0x0'], 'hash': "0x0", 'from': "0x0", 'amount': 100})
    
        assets +=[pool, swap]
        
    if subgraph["type"] == "lending":
        @asset(group_name=slug_, key_prefix=slug_)
        def market(context):
            #use subgraph slug to fetch pools
            return pd.DataFrame({'id': ["0x01"], 'name': "aave USDC"})
        
        @asset(group_name=slug_, key_prefix=slug_)
        def deposit(context):
            #use subgraph slug to fetch pools
            return pd.DataFrame({'id': ['0x0'], 'hash': "0x0", 'account': "0x0", 'amount': 99})
        
        assets +=[market, deposit]

    return assets

subgraphs = [
    {
        "slug": "uniswap-v2-ethereum",
        "type": "dex"
    },
    {
        "slug": "aave-v2-ethereum",
        "type": "lending"
    },    
]

assets = [asset for subgraph in subgraphs for asset in asset_factory(subgraph) ]

def job_factory(rule_def: dict):
    protocol = rule_def["protocol"]
    slug_ = protocol.replace("-", "_")
    rules = rule_def["rules"]
    jobs = []
    for i, rule_dict in enumerate(rules):
        for rule_k, rule_v in rule_dict.items():
            fn = rule_v['fn']
            assets = [SourceAsset([slug_, asset_key]) for asset_key in rule_v['assets']]
            job_name = f"{slug_}__{i}__{rule_k}"
            @job(name=job_name)
            def _job():
                fn(*assets)

            jobs.append(_job)

    return jobs

jobs = [job for rule_def in rules for job in job_factory(rule_def)]