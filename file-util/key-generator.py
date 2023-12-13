with open('wordlist_clean.txt', 'r', encoding='UTF-8') as file:
    with open('wordlist_keys.txt', 'w', encoding='UTF-8') as output:
        for line in file:
            if len(line) <= 7:
                output.write(line)
