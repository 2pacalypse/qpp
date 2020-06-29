select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 24
    and d_year = 1994
    and lo_discount between 5 and 7
    and lo_quantity between 24 and 33
	


