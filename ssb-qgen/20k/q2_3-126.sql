select 
    sum(lo_revenue), d_year, p_brand1
from 
    ssbm_lineorder, ssbm_date, ssbm_part, ssbm_supplier
where 
    lo_orderdate = d_datekey
    and lo_partkey = p_partkey
    and lo_suppkey = s_suppkey
    and p_brand1 = 'MFGR#351'
    and s_region = 'AMERICA'
group by 
    d_year, p_brand1
order by 
    d_year, p_brand1


