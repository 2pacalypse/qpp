select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 35
    and d_year = 1998
    and lo_discount between 7 and 9
    and lo_quantity between 35 and 44
	


