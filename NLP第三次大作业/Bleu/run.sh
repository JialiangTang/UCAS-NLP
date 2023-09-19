for i in {1..30..1}
do
    python ./bleu.py source$i.txt ref$i.txt
done
