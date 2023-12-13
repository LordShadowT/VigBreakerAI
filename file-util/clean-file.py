import csv

with open('wordlist-german.txt', 'r', encoding='UTF-8') as file:
    with open('wordlist_clean.txt', 'w', encoding='UTF-8') as output:
        for line in file:
            modified_line = line.replace('ä', 'ae').replace('Ä', 'Ae')
            modified_line = modified_line.replace('ö', 'oe').replace('Ö', 'Oe')
            modified_line = modified_line.replace('ü', 'ue').replace('Ü', 'Ue')
            modified_line = modified_line.replace('ß', 'ss')
            try:
                output.write(modified_line)
            except:
                print(modified_line)
                break
