select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 24
    and d_year = 1995
    and lo_discount between 3 and 5
    and lo_quantity between 7 and 16
	


