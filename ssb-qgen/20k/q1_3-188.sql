select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 30
    and d_year = 1998
    and lo_discount between 8 and 10
    and lo_quantity between 25 and 34
	


