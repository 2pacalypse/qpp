select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 36
    and d_year = 1992
    and lo_discount between 8 and 10
    and lo_quantity between 36 and 45
	


