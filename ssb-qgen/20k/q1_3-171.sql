select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 13
    and d_year = 1995
    and lo_discount between 0 and 2
    and lo_quantity between 8 and 17
	


