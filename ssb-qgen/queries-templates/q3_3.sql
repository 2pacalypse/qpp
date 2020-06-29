select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    customer, lineorder, supplier, dates
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city=[CI1] or c_city=[CI2])
    and (s_city=[CI1] or s_city=[CI2])
    and d_year >= [YL] and d_year <= [YH]
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc;