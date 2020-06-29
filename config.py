#from utils import get_tables, get_columns

ssb_qgen_dir = '/scratch/mtopak/ssb-qgen'
query_out_dir = '/scratch/mtopak/30'



data_path = '/scratch/data/ssbm100/'
word2vec_model_path = '/scratch/mtopak/files/model.w2v'


catalog_path = '/scratch/data/ssbm100/catalog.json'

host='http://localhost:8888'


op_names = ['PelagoTableScan', 'PelagoAggregate', 'PelagoToEnumerableConverter', 'PelagoSort', 'PelagoUnpack', 'PelagoFilter', 'PelagoJoin', 'PelagoProject', 'PelagoPack', 'PelagoRouter']

table_sizes = {'ssbm10_customer': 300000,
 'ssbm10_date': 2556,
 'ssbm10_lineorder': 59986214,
 'ssbm10_part': 800000,
 'ssbm10_supplier': 20000,
 'ssbm_customer': 3000000,
 'ssbm_date': 2556,
 'ssbm_lineorder': 600038145,
 'ssbm_part': 1400000,
 'ssbm_supplier': 200000}


tables = ['ssbm_lineorder', 'ssbm_date', 'ssbm_customer', 'ssbm_part', 'ssbm_supplier']
columns = {'ssbm_customer': ['c_custkey',
                   'c_name',
                   'c_address',
                   'c_city',
                   'c_nation',
                   'c_region',
                   'c_phone',
                   'c_mktsegment'],
 'ssbm_date': ['d_datekey',
               'd_date',
               'd_dayofweek',
               'd_month',
               'd_year',
               'd_yearmonthnum',
               'd_yearmonth',
               'd_daynuminweek',
               'd_daynuminmonth',
               'd_daynuminyear',
               'd_monthnuminyear',
               'd_weeknuminyear',
               'd_sellingseason',
               'd_lastdayinweekfl',
               'd_lastdayinmonthfl',
               'd_holidayfl',
               'd_weekdayfl'],
 'ssbm_lineorder': ['lo_orderkey',
                    'lo_linenumber',
                    'lo_custkey',
                    'lo_partkey',
                    'lo_suppkey',
                    'lo_orderdate',
                    'lo_orderpriority',
                    'lo_shippriority',
                    'lo_quantity',
                    'lo_extendedprice',
                    'lo_ordtotalprice',
                    'lo_discount',
                    'lo_revenue',
                    'lo_supplycost',
                    'lo_tax',
                    'lo_commitdate',
                    'lo_shipmode'],
 'ssbm_part': ['p_partkey',
               'p_name',
               'p_mfgr',
               'p_category',
               'p_brand1',
               'p_color',
               'p_type',
               'p_size',
               'p_container',
               'p_stocklevel'],
 'ssbm_supplier': ['s_suppkey',
                   's_name',
                   's_address',
                   's_city',
                   's_nation',
                   's_region',
                   's_phone']}


ops = ['<', '>', '>=', '<=', '=']

#tables = get_tables()
#columns = get_columns()
#get_op_names()
