select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    lineorder, dates
where 
    lo_orderdate = d_datekey
    and d_year = [Y]
    and lo_discount between [DL] and [DH]
    and lo_quantity [COMP] 25;
