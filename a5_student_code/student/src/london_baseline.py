# Calculate the accuracy of a baseline that simply predicts "London" for every
#   example in the dev set.
# Hint: Make use of existing code.
# Your solution here should only be a few lines.
with open("birth_dev.tsv", encoding='utf-8') as fin:
    lines = [x.strip().split('\t') for x in fin]
    if len(lines[0]) == 1:
      print('No gold birth places provided; returning (0,0)')
    true_places = [x[1] for x in lines]
    total = len(true_places)
    predicted_places=['London' for i in range(len(true_places))]
    correct = len(list(filter(lambda x: x[0] == x[1],
      zip(true_places, predicted_places))))
    print(float(correct)/float(total))