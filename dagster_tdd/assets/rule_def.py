from .rule_fn import tvl_is_positive, tvl_is_negative, check_dex_pool_fields, check_lending_market_fields, check_protocol_fields, check_amount_is_positive

rules = [
    {
    'protocol': "aave-v2-ethereum", 
    'rules': [
    { 'tvl_is_positive': {'fn': tvl_is_positive, 'assets': ['protocol']}},
    { 'tvl_is_negative_fail': {'fn': tvl_is_negative, 'assets': ['protocol']}},
    { 'deposit_amount_is_positive': {'fn': check_amount_is_positive, 'assets': ['deposit']}},
    { 'check_protocol_fields': {'fn': check_protocol_fields, 'assets': ['protocol']} },
    { 'check_market_fields': {'fn': check_lending_market_fields, 'assets': ['market']} }
    ]},
    {'protocol': "uniswap-v2-ethereum", 
    'rules': [
    { 'tvl_is_positive': {'fn': tvl_is_positive, 'assets': ['protocol']}},
    { 'tvl_is_negative_fail': {'fn': tvl_is_negative, 'assets': ['protocol']}},
    { 'swap_amount_is_positive': {'fn': check_amount_is_positive, 'assets': ['swap']}},
    { 'check_protocol_fields': {'fn': check_protocol_fields, 'assets': ['protocol']} },
    { 'check_pool_fields': {'fn': check_dex_pool_fields, 'assets': ['pool']} }
    ]},
]