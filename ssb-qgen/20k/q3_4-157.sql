select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    ssbm_customer, ssbm_lineorder, ssbm_supplier, ssbm_date
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city='ETHIOPIA 4' or c_city='KENYA    7')
    and (s_city='ETHIOPIA 4' or s_city='KENYA    7')
    and d_yearmonth = 'Oct1995'
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc


