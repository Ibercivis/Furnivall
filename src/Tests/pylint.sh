
print_scores(){
    for i in Core/*.py  ; do
        echo "$i -->" $(pylint $i 2>/dev/null|awk '/rated/ {print $7 }'|cut -d\/ -f1); 
    done
}

total=0;
get_scores(){
    for i in Core/*.py  ; do
        export total=$(($total + 1 ))
        echo "+" $(pylint $i 2>/dev/null|awk '/rated/ {print $7 }'|cut -d\/ -f1); 
    done

}

get_total(){
    ls -1 Core/*py|wc -l
}
print_scores
echo $(( ( 0 $( get_scores | cut -d. -f1 ) ) / $(get_total) ))
