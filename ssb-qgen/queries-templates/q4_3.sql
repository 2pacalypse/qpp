select 
    d_year, s_city, p_brand,
    sum(lo_revenue - lo_supplycost) as profit
from 
    DATES, CUSTOMER, SUPPLIER, PART, LINEORDER
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_partkey = p_partkey
    and lo_orderdate = d_datekey
    and s_nation = [N]
    and (d_year = [Y1] or d_year = [Y2])
    and p_category = [C]
group by 
    d_year, s_city, p_brand
order by 
    d_year, s_city, p_brand;