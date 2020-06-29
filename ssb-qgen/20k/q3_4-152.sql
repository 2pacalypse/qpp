select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    ssbm_customer, ssbm_lineorder, ssbm_supplier, ssbm_date
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city='EGYPT    4' or c_city='KENYA    2')
    and (s_city='EGYPT    4' or s_city='KENYA    2')
    and d_yearmonth = 'Nov1997'
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc

