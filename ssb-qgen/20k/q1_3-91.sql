select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 39
    and d_year = 1992
    and lo_discount between 1 and 3
    and lo_quantity between 10 and 19
	


