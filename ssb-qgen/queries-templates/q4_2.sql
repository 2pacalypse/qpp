select 
    d_year, s_nation, p_category,
    sum(lo_revenue - lo_supplycost) as profit
from 
    DATES, CUSTOMER, SUPPLIER, PART, LINEORDER
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_partkey = p_partkey
    and lo_orderdate = d_datekey
    and c_region = [R]
    and s_region = [R]
    and (d_year = [Y1] or d_year = [Y2])
    and (p_mfgr = [MFGR1] or p_mfgr = [MFGR2])
group by 
    d_year, s_nation, p_category
order by 
    d_year, s_nation, p_category;