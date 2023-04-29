printf "##########\nTest1 elvart:\nABC-AB\n5\nValodi:\n"
printf "1,2,3,-1,5,-1\n" | python ./main.py
printf "\n##########\nTest2 elvart:\nABC*A-\n5\nValodi:\n"
printf "1,2,3,5,4,2\n" | python ./main.py 
printf "\n##########\nTest3 elvart:\nABC-A--B\n5\nValodi:\n"
printf "1,2,3,2,4,3,2,1\n" | python ./main.py
printf "\n##########\nTest4 elvart:\nABC-ABC*\n7\nValodi:\n"
printf "1,2,3,3,4,5,2,1\n" | python ./main.py
printf "\n##########\nTest5 elvart:\nABC*AB-CA\n8\nValodi:\n"
printf "1,2,3,4,5,4,3,2,1\n" | python ./main.py
#printf "\n##########\nTest6 elvart:\nAB-C-A-\n4\nValodi:\n"
#printf "-5,2,5,3,2,1,-3\n" | python ./main.py
printf "\n##########\nTest7 VEGSO elvart:\nABC*-B--CB\n7\nValodi:\n"
printf "1,2,3,4,1,5,1,3,6,3\n" | python ./main.py
read
