select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    ssbm_customer, ssbm_lineorder, ssbm_supplier, ssbm_date
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city='EGYPT    0' or c_city='INDONESIA0')
    and (s_city='EGYPT    0' or s_city='INDONESIA0')
    and d_yearmonth = 'Mar1993'
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc


