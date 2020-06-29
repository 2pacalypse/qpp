#!/bin/sh
#Needs the ./dists directory
#Needs the ./queries-templates directory
#Syntax: qgen.sh <qid> <seed>(optional)
#<qid> has the form q1_1, q1_2, ..., q2_1, ... etc
#if no seed given seeding is based on time (with granularity of seconds)

QUERY_TEMPLATES_DIR="./queries-templates"
DISTS_DIR="./dists"

if [ ! -d $DISTS_DIR ]
then
	echo "$0: There is no directory with the distributions (${DISTS_DIR})"
	exit
fi


if [ ! -d $QUERY_TEMPLATES_DIR ]
then
	echo "$0: There is no directory with the query templates (${QUERY_TEMPLATES_DIR})"
	exit
fi


if [ $# -eq 1 ]
then
	QUERY=${QUERY_TEMPLATES_DIR}/$1
	SEED=`date +%s`
elif [ $# -eq 2 ]
then
	QUERY=${QUERY_TEMPLATES_DIR}/$1
	SEED=$2 #This is used for seeding.

else
	echo "$0: Please give query id."
	echo "$0: Syntax is: $0 qid <seed>"
	exit
fi

cd dists


NoY=`cat years.dss | wc -l`
NoD=`cat discounts.dss | wc -l`
NoCI=`cat cities.dss | wc -l`
NoQ=`cat quantities.dss | wc -l`
NoR=`cat regions.dss | wc -l`
NoN=`cat nations.dss | wc -l`
NoWNY=`cat weeknumsinyear.dss | wc -l`
NoYM=`cat yearmonths.dss | wc -l`
NoYMN=`cat yearmonthnums.dss | wc -l`
NoC=`cat categories.dss | wc -l`
NoMFGR=`cat mfgrs.dss | wc -l`
NoB=`cat brands.dss | wc -l`
NoCOMP=`cat comparisons.dss | wc -l`

RANDOM=$SEED

#set -x

YY=`cat years.dss | awk -v rnd=$RANDOM -v max=$NoY -v limit=5 'BEGIN{ind=1+rnd%(max-limit);}{if (NR==ind || NR==(ind+limit)) print $0;}'`
set - $YY
YL=$1
YH=$2
Y=`cat years.dss | awk -v rnd=$RANDOM -v max=$NoY 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
#set -x
YYY=`cat years.dss | awk -v rnd=$RANDOM -v rnd2=$RANDOM -v max=$NoY 'BEGIN{ind=1+rnd%max; ind2=1+(rnd+rnd2)%max; if (ind==ind2) ind2=1+(ind2+1)%max;}{if (NR==ind || NR==ind2) print $0;}'`
set - $YYY
Y1=$1
Y2=$2
YMN=`cat yearmonthnums.dss | awk -v rnd=$RANDOM -v max=$NoYMN 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
tempYM=`cat yearmonths.dss | awk -v rnd=$RANDOM -v max=$NoYM 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
YM=`echo "'$tempYM'"`
WNY=`cat weeknumsinyear.dss | awk -v rnd=$RANDOM -v max=$NoWNY 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`

DD=`cat discounts.dss | awk -v rnd=$RANDOM -v max=$NoD -v limit=2 'BEGIN{ind=1+rnd%(max-limit);}{if (NR==ind || NR==(ind+limit)) print $0;}'`
set - $DD
DL=$1
DH=$2

COMP=`cat comparisons.dss | awk -v rnd=$RANDOM -v max=$NoCOMP 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`

QQ=`cat quantities.dss | awk -v rnd=$RANDOM -v max=$NoQ -v limit=9 'BEGIN{ind=1+rnd%(max-limit);}{if (NR==ind || NR==(ind+limit)) print $0;}'`
set - $QQ
QL=$1
QH=$2

tempR=`cat regions.dss | awk -v rnd=$RANDOM -v max=$NoR 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
R=`echo "'$tempR'"`

tempC=`cat categories.dss | awk -v rnd=$RANDOM -v max=$NoC 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
C=`echo "'$tempC'"`

BB=`cat brands.dss | awk -v rnd=$RANDOM -v max=$NoB -v limit=7 'BEGIN{ind=1+rnd%(max-limit);}{if (NR==ind || NR==(ind+limit)) print $0;}'`
set - $BB
tempBL=$1
BL=`echo "'$tempBL'"`
tempBH=$2
BH=`echo "'$tempBH'"`
tempB=`cat brands.dss | awk -v rnd=$RANDOM -v max=$NoB 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
B=`echo "'$tempB'"`

CICI=`cat cities.dss | awk -v rnd=$RANDOM -v rnd2=$RANDOM -v max=$NoCI 'BEGIN{ind=1+rnd%max; ind2=1+(rnd+rnd2)%max; if(ind==ind2) ind2=1+(ind2+1)%max;}{if (NR==ind || NR==ind2) {gsub(" ","%");print $0;}}'`
set - $CICI
tempCI1=`echo $1 | awk '{gsub("%"," ");print $0;}'`
tempCI2=`echo $2 | awk '{gsub("%"," ");print $0;}'`
CI1=`echo "'$tempCI1'"`
CI2=`echo "'$tempCI2'"`

MFMF=`cat mfgrs.dss | awk -v rnd=$RANDOM -v rnd2=$RANDOM -v max=$NoMFGR 'BEGIN{ind=1+rnd%max; ind2=1+(rnd+rnd2)%max; if (ind==ind2) ind2=1+(ind2+1)%max;}{if (NR==ind || NR==ind2) print $0;}'`
set - $MFMF
tempMFGR1=$1
tempMFGR2=$2
MFGR1=`echo "'$tempMFGR1'"`
MFGR2=`echo "'$tempMFGR2'"`

tempN=`cat nations.dss | awk -v rnd=$RANDOM -v max=$NoN 'BEGIN{ind=1+rnd%max;}{if (NR==ind) print $0;}'`
N=`echo "'$tempN'"`


cd ..

DEBUG=0
if [ $DEBUG -eq 1 ]
then
echo Should be 23
echo $Y
echo $Y1
echo $Y2
echo $YL
echo $YH
echo $DL
echo $DH
echo $COMP
echo $QL
echo $QH
echo $YMN
echo $WNY
echo $R
echo $C
echo $BL
echo $BH
echo $B
echo $CI1
echo $CI2
echo $YM
echo $MFGR1
echo $MFGR2
echo $N
echo "End of params"
fi




#set -x

cat ${QUERY}.sql | \
awk -v val="$N" '{gsub(/\[N\]/,val); print $0}' | \
awk -v val="$Y" '{gsub(/\[Y\]/,val); print $0}' | \
awk -v val="$Y1" '{gsub(/\[Y1\]/,val); print $0}' | \
awk -v val="$Y2" '{gsub(/\[Y2\]/,val); print $0}' | \
awk -v val="$YL" '{gsub(/\[YL\]/,val); print $0}' | \
awk -v val="$YH" '{gsub(/\[YH\]/,val); print $0}' | \
awk -v val="$DL" '{gsub(/\[DL\]/,val); print $0}' | \
awk -v val="$DH" '{gsub(/\[DH\]/,val); print $0}' | \
awk -v val="$COMP" '{gsub(/\[COMP\]/,val); print $0}' | \
awk -v val="$QL" '{gsub(/\[QL\]/,val); print $0}' | \
awk -v val="$QH" '{gsub(/\[QH\]/,val); print $0}' | \
awk -v val="$YMN" '{gsub(/\[YMN\]/,val); print $0}' | \
awk -v val="$WNY" '{gsub(/\[WNY\]/,val); print $0}' | \
awk -v val="$R" '{gsub(/\[R\]/,val); print $0}' | \
awk -v val="$C" '{gsub(/\[C\]/,val); print $0}' | \
awk -v val="$BL" '{gsub(/\[BL\]/,val); print $0}' | \
awk -v val="$BH" '{gsub(/\[BH\]/,val); print $0}' | \
awk -v val="$B" '{gsub(/\[B\]/,val); print $0}' | \
awk -v val="$CI1" '{gsub(/\[CI1\]/,val); print $0}' | \
awk -v val="$CI2" '{gsub(/\[CI2\]/,val); print $0}' | \
awk -v val="$YM" '{gsub(/\[YM\]/,val); print $0}' | \
awk -v val="$MFGR1" '{gsub(/\[MFGR1\]/,val); print $0}' | \
awk -v val="$MFGR2" '{gsub(/\[MFGR2\]/,val); print $0}' 


echo

#set +x

