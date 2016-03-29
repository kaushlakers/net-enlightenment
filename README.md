To Run:
Python Code in:
/home/3/ramachsh/Acads/5245/assignments/lab2/net-enlightenment

The graph data files are in:
/home/3/ramachsh/Acads/5245/assignments/data_lab2
(Each graph has it's own folder)

Navigate to python folder and execute:

for i in `find /home/3/ramachsh/Acads/5245/assignments/data_lab2/ *.adjlist`;do python net_enlightener.py $i UNDIRECTED; done
for i in `find /home/3/ramachsh/Acads/5245/assignments/data_lab2/ *.txt`;do python net_enlightener.py $i UNDIRECTED; done

For running the entropy stuff, run
for i in `find /home/3/ramachsh/Acads/5245/assignments/data_lab2/com-youtube.ungraph/ *.c1000*`;do  python net_enlightener.py /home/3/ramachsh/Acads/5245/assignments/data_lab2/com-youtube.ungraph.adjlist UNDIRECTED $i /home/3/ramachsh/Acads/5245/assignments/data_lab2/com-youtube.ungraph/com-youtube.ungraph.metis.GT; done
