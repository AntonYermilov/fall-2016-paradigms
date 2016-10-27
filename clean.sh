find * -type d | while read d; do
	#value = echo `expr match "$d" ".*"`
	if [[ $d =~ .*__pycache__ ]]; then
		echo $d
		rm -rf $d
	fi
done
