select 
    c_nation, s_nation, d_year,
    sum(lo_revenue) as revenue
from 
    customer, lineorder, supplier, dates
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and c_region = [R]
    and s_region = [R]
    and d_year >= [YL] and d_year <= [YH]
group by 
    c_nation, s_nation, d_year
order by 
    d_year asc, revenue desc;
