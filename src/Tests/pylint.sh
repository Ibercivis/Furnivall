for i in Core/*.py  ; do echo "$i: "  $(pylint $i 2>/dev/null|awk '/rated/ {print $7 }'|cut -d\/ -f1); done
