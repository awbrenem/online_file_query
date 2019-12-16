#! /bin/bash
#
# Runs IDL rbsp_efw_l2_driver_custom batch job
# Usage: ./rbsp_efw_l2_driver_custom.bash

#DATE=`date -j +%Y%m%d`
#DATEFILE=~fishing/logs/external/rbsp-sync-timestamp
#if [ -e $DATEFILE ]; then
#   while [ `date -j -f%s +%Y%m%d $(stat -f%m $DATEFILE)` != "$DATE" ]; do
#        echo "Waiting for $DATEFILE at `date`"
#        sleep 300
#    done
#else
#    echo "Unable to find timestamp file $DATEFILE; continuing anyway..."
#fi

export PATH=$PATH:/opt/local/bin:/opt/local/sbin
source /Applications/exelis/idl/bin/idl_setup.bash
unset IDL_PATH
export CDF_LEAPSECONDSTABLE=CDFLeapSeconds.txt
export TDAS_RBSP=$HOME/Code/tdas_svn
export RBSP_L2_HOME=$HOME/RBSP_l2
export IDL_DLM_PATH=$RBSP_HOME:+/Applications/exelis/idl/bin/bin.darwin.x86_64
export IDL_PATH=+.:+$TDAS_RBSP:+/Applications/exelis/idl/lib:+/Applications/exelis/idl/examples/doc/utilities
cd $RBSP_L2_HOME

starttime=`date +%s`

# update the skeleton CDFs in the l2/xxxx/0000/ dirs
#./rbsp_update_l2_skeleton.bash

i=1435
istop=1435
bp_rbspa=34  #boom pair
bp_rbspb=12
version=2
bad_probe_rbspa=1
bad_probe_rbspb=0

TTAG=`date +%s`
TEMPDIR="$HOME/l2temp.$TTAG"

while [ $i -le $istop ]; do

	let newdate=starttime-i*86400
	yyyy=`date -j -f "%s" +%Y $newdate`
	doy=`date -j -f "%s" +%j $newdate`

#---------------------------
#	for p in a b; do	
#---------------------------
        for p in a; do

		PROBE=$p

                if [ "$PROBE" == "a" ]; then
                        bp="$bp_rbspa"
			bad_probe="$bad_probe_rbspa"
                else
                        bp="$bp_rbspb"
			bad_probe="$bad_probe_rbspb"
                fi


		OUTLOG=$HOME/RBSP_l2/log/rbsp_efw_l2_driver_custom_${yyyy}-${doy}_rbsp${PROBE}_output.log
		/Applications/exelis/idl/bin/idl rbsp_efw_l2_driver_custom -args \
		$yyyy $doy $PROBE $TEMPDIR $bp $version $bad_probe 2>&1 | grep -v STORE_DATA --line-buffered \
		| grep -v Processing --line-buffered \
		| grep -v GEOPACK_RECALC --line-buffered &>$OUTLOG

	done

	# transfer
	DATETAG=$yyyy-$doy
	TRANSFERLOG=$HOME/RBSP_l2/log/l2_transfer_custom_$DATETAG.log
	/usr/bin/rsync -az --log-file=$TRANSFERLOG \
	     $TEMPDIR/ /Volumes/DataA/user_volumes/kersten/data/rbsp/

	/bin/rm -vrf $TEMPDIR

	let i=i+1

done

/bin/rm -vrf $TEMPDIR

