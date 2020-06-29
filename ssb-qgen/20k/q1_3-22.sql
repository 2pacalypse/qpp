select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 23
    and d_year = 1993
    and lo_discount between 4 and 6
    and lo_quantity between 23 and 32
	


