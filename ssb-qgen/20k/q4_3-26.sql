select 
    d_year, s_city, p_brand1,
    sum(lo_revenue - lo_supplycost) as profit
from 
    ssbm_date, ssbm_customer, ssbm_supplier, ssbm_part, ssbm_lineorder
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_partkey = p_partkey
    and lo_orderdate = d_datekey
    and s_nation = 'ARGENTINA'
    and (d_year = 1995 or d_year = 1997)
    and p_category = 'MFGR#12'
group by 
    d_year, s_city, p_brand1
order by 
    d_year, s_city, p_brand1


