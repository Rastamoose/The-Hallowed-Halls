myList = [3,5,1,12,7,87,9]

print(myList)

def bubble_sort(list):
  swapped = True
  while swapped:
    swapped = False
    for i in range(len(myList)- 1) :  #stops 1 before last element as last has nothing to compare with
      if list[i] > list[i+1]:
        to_swap = list[i]       
        list[i] = list[i+1]        #swaps elements
        list[i+1] = to_swap
        swapped = True
  


bubble_sort(myList)

print(myList)




file = open("my_animals.txt","w+") 
file.write("fat \n\n")
file.write("blob")
file_contents = file.read()
for line in file:
  current_line = line
  print(line)
file.close()
print(file_contents)