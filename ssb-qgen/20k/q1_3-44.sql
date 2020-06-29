select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 45
    and d_year = 1994
    and lo_discount between 8 and 10
    and lo_quantity between 4 and 13
	

