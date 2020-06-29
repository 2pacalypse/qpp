select 
    sum(lo_extendedprice*lo_discount) as revenue
from 
    ssbm_lineorder, ssbm_date
where 
    lo_orderdate = d_datekey
    and d_weeknuminyear = 28
    and d_year = 1992
    and lo_discount between 7 and 9
    and lo_quantity between 11 and 20
	


