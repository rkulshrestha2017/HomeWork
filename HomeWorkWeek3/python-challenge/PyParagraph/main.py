import os
import string

#Choose File Number (1 or 2)
file_num = 2

#sets file
file = os.path.join('Resources', 'paragraph_' + str(file_num) + '.txt')

# Open and reads file and saves text as paragraph string?
paragraph_str = ''
with open(file, 'r') as txtfile:
    paragraph_str = txtfile.read()


#Sentence count by counting ., ? and !
sen_count = paragraph_str.count('.') + paragraph_str.count('?') + paragraph_str.count('!')

#Creates a string of upper and lowercase letters
letters = string.ascii_letters + " " 

#Loops through paragraph string and deletes all characters 
# that are not letters replacing with nothing
for char in paragraph_str:
    if char not in letters:
        paragraph_str = paragraph_str.replace(char,'')


#Reassigns the paragraph string and makes a list of words by splitting at spaces
paragraph_list = paragraph_str.split(" ")

#Counts all of the letters in list paragraph
letter_total = 0
for word in paragraph_list:
    letter_total += len(word)

#Counts words by counting the length of paragraph list
word_count = len(paragraph_list)

#Calculates average word length by dividing the total # of letters
#By the number of words
avg_word_length = letter_total/word_count

#Calculates words per sentence by dividing the number of words by the number of sentences.
words_per_sentence = word_count/sen_count

#Sets output file 
output_file = os.path.join('OutputFiles', 'paragraph_analysis_file' + str(file_num)+ '.txt')

#Opens output file and writes to it
with open(output_file, 'w') as txtfile:

    txtfile.writelines('Paragraph Analysis\n-----------------\nApproximate Word Count: ' 
                        + str(word_count)+ '\nApproximate Sentence Count: '+ str(sen_count) + 
                        '\nAverage Letter Count: ' + str(avg_word_length) + 
                        '\nAverage Sentence Length: ' + str(words_per_sentence))

#Opens output file and prints to terminal
with open(output_file, 'r') as txtout:
    print(txtout.read())