select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    ssbm_customer, ssbm_lineorder, ssbm_supplier, ssbm_date
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city='CANADA   9' or c_city='FRANCE   8')
    and (s_city='CANADA   9' or s_city='FRANCE   8')
    and d_yearmonth = 'Jul1996'
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc


