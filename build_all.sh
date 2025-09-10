for i in {1..10}
do
    make clean ASC=$i
    make ASC=$i
done