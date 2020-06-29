select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 8
    and d_year = 1993
    and lo_discount between 5 and 7
    and lo_quantity between 32 and 41
	


