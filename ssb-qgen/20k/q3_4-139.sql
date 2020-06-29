select 
    c_city, s_city, d_year, sum(lo_revenue) as revenue
from 
    ssbm_customer, ssbm_lineorder, ssbm_supplier, ssbm_date
where 
    lo_custkey = c_custkey
    and lo_suppkey = s_suppkey
    and lo_orderdate = d_datekey
    and (c_city='BRAZIL   8' or c_city='JAPAN    9')
    and (s_city='BRAZIL   8' or s_city='JAPAN    9')
    and d_yearmonth = 'Mar1998'
group by 
    c_city, s_city, d_year
order by 
    d_year asc, revenue desc


