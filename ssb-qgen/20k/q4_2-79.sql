select 
    d_year, s_nation, p_category,
    sum(lo_revenue - lo_supplycost) as profit
from 
    ssbm_date, ssbm_customer, ssbm_supplier, ssbm_part, ssbm_lineorder
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_partkey = p_partkey
    and lo_orderdate = d_datekey
    and c_region = 'MIDDLE EAST'
    and s_region = 'MIDDLE EAST'
    and (d_year = 1994 or d_year = 1996)
    and (p_mfgr = 'MFGR#4' or p_mfgr = 'MFGR#5')
group by 
    d_year, s_nation, p_category
order by 
    d_year, s_nation, p_category


