#converts networkx edgelist to normal edgelist
for i in `ls *.edgelist`; do echo $i; grep -o '^n[0-9]\+ n[0-9]\+' $i | sed 's/n//g' > $i.txt; done
#runs cnm on all the edgelists
for i in `ls *.txt`; do ../../cnm/community  -i:$i -o:$i.communities; done
