import json
import random
import os
import copy
import sys
import re
import unicodedata
from alive_progress import alive_bar


cwd = os.getcwd()

#From the Quotable readme file: "Quotable is a free, open source quotations API.
#It was originally built as part of a [FreeCodeCamp](https://www.freecodecamp.org/)
#project. The database includes over 2000 quotes by 900 authors." A subset of 500
#quotes are made available to the public for use according to the terms of a MIT license.
with open(os.path.join(cwd, "quotable-master", "data", "sample", "quotes.json"), encoding="utf-8") as q:
    quotes = json.load(q)
    with open(os.path.join(cwd, "quotable-master", "data", "sample", "authors.json"), encoding="utf-8") as a:
        authors = json.load(a)

    #Populating the list "quotes_and_authors" with lists containing the
    #quote as the first list element and the author as the second one.
    quotes_and_authors = []
    for i in range(len(quotes)):
        quotes_and_authors.append([quotes[i]['content'], quotes[i]['author']])

#The "number_of_cryptograms" variable represents the number of different
#quotes generated with different ciphers and is initialized to 1.
number_of_cryptograms = 1
#The "number_of_columns" variable designates the number of braille characters
#per line, including empty braille cells. "number_of_rows" maps to the number
#of lines per page. The default values for "number_of_columns" and
#"number_of_rows" are 32 and 25, respectively, which corresponds to the
#embossing parameters for 8 1/2" by 11" pages.
number_of_columns = 32
number_of_rows = 25
#The "hint_list" list is initialized as an empty list and lists the
#letters that the user wishes to know the cipher result for. The letters
#can be entered individually (separated by spaces) as additional arguments
#during the Python call or "hints26" can be entered as an additional
#argument to provide results for all leters of the cipher.
hint_list = []
#Instead of generating a cryptogram using the built-in quotes from the
#Quotable dataset, the user can input some text at least 80 characters
#in length (including spaces) and containing standard punctuation marks.
user_text = []
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if arg.isdigit():
            number_of_cryptograms = int(arg)
        elif len(arg) == 1 and arg.isalpha():
            hint_list += [arg]
        elif arg[:3] == "row" and arg[3:].isdigit():
            number_of_rows = int(arg[3:])
        elif arg[:3] == "col" and arg[3:].isdigit():
            number_of_columns = int(arg[3:])
        elif arg.lower() == "hints26":
            hint_list = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
            "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
        elif len(arg) > 3 and arg[:3] != "row" and arg[:3] != "col" and arg.lower() != "hints26":
            user_text = [arg]
            number_of_cryptograms = 1

braille_letters_sorted = ["⠁", "⠃", "⠉", "⠙", "⠑", "⠋", "⠛", "⠓", "⠊", "⠚", "⠅",
"⠇", "⠍", "⠝", "⠕", "⠏", "⠟", "⠗", "⠎", "⠞", "⠥", "⠧", "⠺", "⠭", "⠽", "⠵"]

braille_alphabet = {"a":"⠁", "b":"⠃", "c":"⠉", "d":"⠙", "e":"⠑", "f":"⠋", "g":"⠛", "h":"⠓", "i":"⠊", "j":"⠚",
"k":"⠅", "l":"⠇", "m":"⠍", "n":"⠝", "o":"⠕", "p":"⠏", "q":"⠟", "r":"⠗", "s":"⠎", "t":"⠞", "u":"⠥", "v":"⠧",
"w":"⠺", "x":"⠭", "y":"⠽", "z":"⠵"}

braille_alphabet_punctuation = {"a":"⠁", "b":"⠃", "c":"⠉", "d":"⠙", "e":"⠑", "f":"⠋", "g":"⠛", "h":"⠓", "i":"⠊",
"j":"⠚", "k":"⠅", "l":"⠇", "m":"⠍", "n":"⠝", "o":"⠕", "p":"⠏", "q":"⠟", "r":"⠗", "s":"⠎", "t":"⠞", "u":"⠥",
"v":"⠧", "w":"⠺", "x":"⠭", "y":"⠽", "z":"⠵", ",":"⠂", ".":"⠲", ":":"⠒", ";":"⠆", "-":"⠤", "–":"⠠⠤", "—":"⠐⠠⠤",
"!":"⠖", "?":"⠦", "…":"⠲⠲⠲", "«":"⠸⠦", "“":"⠘⠦", '"':"⠠⠶", "‘":"⠠⠦", "'":"⠄", "»":"⠸⠴", "”":"⠘⠴", "’":"⠠⠴",
"(":"⠐⠣", ")":"⠐⠜", "[":"⠨⠣", "]":"⠨⠜", "{":"⠸⠣", "}":"⠸⠜"}

#The list "done_quotes" indicates which quotes have already been converted
#into cryptograms, so as to avoid repeating them.
done_quotes = []
#The list "unacceptable_quotes" lists the indices of the quotes that do not
#meet the length criteria for further processing, namely a character length
#of at least 80 characters and a number of rows that can be accomodated within
#one page at the specified "number_of_rows".
unacceptable_quotes = []
#The "i in range(number_of_cryptograms)" loop proceeds as many times as
#required to generate the number of cryptograms specified in "number_of_cryptograms",
#insofar as all of the 500 available quote indices (len(quotes_and_authors)) have not
#already been appended to the "done_quotes" or "unacceptable_quotes" lists, meaning
#that there are no more cryptograms that can be generated without selecting the same quote twice.
with alive_bar(number_of_cryptograms) as bar:
    for i in range(number_of_cryptograms):
        if len(done_quotes) + len(unacceptable_quotes) < len(quotes_and_authors):
            cipher = {}
            #The "while" loop runs until the dictionary "cipher"
            #contains every letter key and its associated encrypted
            #value.
            while len(cipher) < len(braille_letters_sorted):
                cipher = {}
                #The list "done_k_indices" will record the encrypted letter
                #values that have already been assigned, in order to avoid
                #duplicate values in the cipher.
                done_k_indices = []
                #The "shuffled_indices" list is assembled by randomly selecting indices within the range
                #of the "braille_letters_sorted" list, without repeats, using the "random.sample()" method.
                shuffled_indices = random.sample(range(len(braille_letters_sorted)), len(braille_letters_sorted))
                for j in range(len(braille_letters_sorted)):
                    for k in shuffled_indices:
                        #A value is assigned to a letter within the "cipher"
                        #dictionary only if its index within "braille_letters_sorted"
                        #isn't the same as that of the letter key itself and if it isn't
                        #already in "done_k_indices".
                        if j != k and k not in done_k_indices:
                            cipher[braille_letters_sorted[j]] = braille_letters_sorted[k]
                            done_k_indices.append(k)
                            break
            #The "cipher_list_of_lines" list is populated by adding the key and either
            #the value (if it was among the hints specified in the list "hint_list") or
            #empty braille cells to accomodate braille letter-labelled magnetic push pins
            #on the embossed page. The variable "current_row_length" is initialized at "0"
            #and is incremented by the length of the key and value or empty braille cells,
            #up to the maximal width allowed on the page. The list "cipher_list_of_lines"
            #is initialized as an empty list and will collect the lines as nested lists.
            current_row_length = 0
            cipher_list_of_lines = []
            for key,value in cipher.items():
                #If hint_list is not an empty list, the user has specified some of the letters
                #in the cipher for which they would like to have the encrypted value provided.
                if hint_list != []:
                    for j in range(len(hint_list)):
                        #If "cipher_list_of_lines" already contains nested lists (indicating
                        #that we are not on the first line), and that the text on the current
                        #row (including the 5 spaces required for empty braille cells, the key,
                        #the colon and the value) can fit within the "number_of_columns" deducted
                        #by two spaces for the left and right borders of the box, and that accessing
                        #the "braille_alphabet" dictionary at key "hint_list[j]" gives the key for
                        #value in the "cipher" dictionary (meaning that the user has requested the
                        #answer for that letter), then the key/value pair are added to the row,
                        #and "current_row_length" is incremented by 5 units. A break leaves the
                        #"for j in range(len(hint_list))" loop, as a hint that corresponds to a key
                        #of the "cipher" dictionary under investigation has already been found.
                        if (cipher_list_of_lines != [] and current_row_length + 5 <= number_of_columns - 2 and
                        braille_alphabet[hint_list[j]] == key):
                            cipher_list_of_lines[-1][0] += "⠀" + key + "⠒⠀" + value
                            current_row_length += 5
                            break
                        #If the "braille_alphabet" dictionary at key "hint_list[j]" gives the key for
                        #value in the "cipher" dictionary but the other conditions are not met (either
                        #because it is the first line in "cipher_list_of_lines" or because there isn't
                        #enough space on the current line for the key, value, colon and empty braille
                        #cells), then a new line is started and "current_row_length" is reset to 5 units.
                        #A break leaves the "for j in range(len(hint_list))" loop, as a hint that corresponds
                        #to a key of the "cipher" dictionary under investigation has already been found.
                        elif braille_alphabet[hint_list[j]] == key:
                            cipher_list_of_lines.append(["⠀" + key + "⠒⠀" + value])
                            current_row_length = 5
                            break
                        #If the last hint in "hint_list" is under investigation and there is already at
                        #least one line in the "cipher_list_of_lines" list and there is enough room left
                        #in the current line to accomodate three empty braille cells in addition to the
                        #key and a colon, and the "braille_alphabet" dictionary at key "hint_list[j]"
                        #doesn't give the key for value in the "cipher" dictionary (meaning that the user
                        #didn't request the answer for this letter) then the row is added to the current
                        #line and "current_row_length" is incremented by 6 units. A break leaves the
                        #"for j in range(len(hint_list))" loop, as a hint that corresponds to a key of
                        #the "cipher" dictionary under investigation has already been found.
                        elif (j == len(hint_list)-1 and cipher_list_of_lines != [] and
                        current_row_length + 6 <= number_of_columns - 2 and braille_alphabet[hint_list[j]] != key):
                            cipher_list_of_lines[-1][0] += "⠀" + key + "⠒⠀⠀⠀"
                            current_row_length += 6
                            break
                        #If the last hint in "hint_list" is under investigation and the "braille_alphabet"
                        #dictionary at key "hint_list[j]" doesn't give the key for value in the "cipher"
                        #dictionary (meaning that the user didn't request the answer for this letter), then
                        #the three empty braille cells in addition to the key and a colon are appended to
                        #"cipher_list_of_lines" as a nested list designating a new line. Since the other
                        #condition above (current_row_length + 6 <= number_of_columns - 2) is not met, this
                        #can mean that the first line is under consideration or that there isn't enough room
                        #on the current line to accomodate 6 more characters. The "current_row_length" is reset
                        #to 6 units.
                        if j == len(hint_list)-1 and braille_alphabet[hint_list[j]] != key:
                            cipher_list_of_lines.append(["⠀" + key + "⠒⠀⠀⠀" ])
                            current_row_length = 6
                #If the user hasn't requested any hints, then a similar approach to the above
                #was followed, except that the values were not added along with the keys.
                elif hint_list == []:
                    if cipher_list_of_lines != [] and current_row_length + 6 <= number_of_columns -2:
                        cipher_list_of_lines[-1][0] += "⠀" + key + "⠒⠀⠀⠀"
                        current_row_length += 6
                    else:
                        cipher_list_of_lines.append(["⠀" + key + "⠒⠀⠀⠀" ])
                        current_row_length = 6

            #This function is inspired by the following StackOverflow thread:
            #"https://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-normalize-in-a-python-unicode-string"
            #The function removes any diacritics in the author names, so that they could be
            #be represented in Grade I UEB braille.
            def remove_diacritics(author):
                author_without_diacritics = unicodedata.normalize('NFKD', author)
                return u"".join([c for c in author_without_diacritics if not unicodedata.combining(c)])
            #If the user has provided some text, the "quotes_and_authors" list is overwritten with
            #a list containing the string "user_text".
            if user_text != []:
                quotes_and_authors = [user_text]
            quotes_and_authors_braille = []
            quotes_and_authors_braille_encrypted = []
            #The nested for loops below investigate every quote and author
            #printed English strings. If the user hasn't provided their own text
            #and that the second element of a sublist is under investigation
            #(meaning that it is the author name), it will be submitted to the
            #function "remove_diacritics()" in case it contained characters not
            #found in grade I UEB braille. The "lower()" method is used on every
            #string because the dictionaries only contain the lowercase letters
            for j in range(len(quotes_and_authors)):
                for k in range(len(quotes_and_authors[j])):
                    if user_text == [] and k == 1:
                        english_text_string = remove_diacritics(quotes_and_authors[j][k].lower())
                    else:
                        english_text_string = quotes_and_authors[j][k].lower()
                    #The printed English strings are transcribed into grade I braille. The unencrypted
                    #grade I braille strings are added to the "quotes_and_authors_braille" list.
                    mapping_table_braille = english_text_string.maketrans(braille_alphabet_punctuation)
                    braille_text_string = english_text_string.translate(mapping_table_braille)
                    if quotes_and_authors_braille != []:
                        quotes_and_authors_braille[-1].extend([braille_text_string])
                    else:
                        quotes_and_authors_braille.append([braille_text_string])
                    #The shuffled/encrypted grade I braille strings are added to the
                    #"quotes_and_authors_braille_encrypted" list. Instances of regular
                    #spaces are changed for empty braille cells ("⠀").
                    mapping_table_braille_shuffled = braille_text_string.maketrans(cipher)
                    braille_text_string_encrypted = (
                    braille_text_string.translate(mapping_table_braille_shuffled).replace(" ", "⠀"))
                    #An empty braille cell is inserted in-between every braille character to accomodate for the
                    #braille letter-labelled magnetic push pins on the embossed pages. Any instances of two or
                    #more empty braille cells (which were originally regular spaces in the printed English string)
                    #are changed for a forward slash ("⠸⠌") braille divider, as it would otherwise be difficult to
                    #locate spaces between words with the other added empty braille cells in-between the characters
                    #making up the words themselves.
                    braille_text_string_encrypted_with_spacers = (
                    "⠀".join([char for char in braille_text_string_encrypted]))
                    braille_text_string_encrypted_with_spacers = (
                    re.sub('["⠀"]{2,}', "⠸⠌", braille_text_string_encrypted_with_spacers))
                    if quotes_and_authors_braille_encrypted != []:
                        quotes_and_authors_braille_encrypted[-1].extend([braille_text_string_encrypted_with_spacers])
                    else:
                        quotes_and_authors_braille_encrypted.append([braille_text_string_encrypted_with_spacers])
                #After a quote and its author have been added to the lists "quotes_and_authors_braille_encrypted"
                #and "quotes_and_authors_braille", an empty list is added to start a new nested list for another
                #quote/author pair, except for the last entry of the "quotes_and_authors" list.
                if j < len(quotes_and_authors)-1:
                    quotes_and_authors_braille_encrypted.append([])
                    quotes_and_authors_braille.append([])

            #The list "randomized_indices" is populated by sampling the numbers within the range of the length of
            #the "quotes_and_authors_braille_encrypted" list, without duplicates, using the "random.sample()" method.
            randomized_indices = (random.sample(range(len(quotes_and_authors_braille_encrypted)),
            len(quotes_and_authors_braille_encrypted)))
            for j in randomized_indices:
                #If the random index under investigation has not already been
                #used to create a cryptogram (present in "done_quotes") or has
                #not already been deemed inadequate to pursue (already in
                #unacceptable_quotes), then it is stored in the variable
                #"encrypted_quote_author_index" for use outside of the "for"
                #loops. The encrypted quote is stored in the variable
                #"encrypted_quote" and indices of all the forward slash
                #delimitors ("⠸⠌") are collected using "re.finditer"
                #and doing a list comprehension of the "match.start()"
                #elements. The list "quote_line_list" is initialised
                #as an empty list and will contain every line of the
                #encrypted quote, according to the specified "number_of_columns".
                #The variable "current_row_length" will keep tabs of the
                #length of the line sublist being currently assembled
                #and will determine when to start a new line (new sublist).
                if j not in done_quotes and j not in unacceptable_quotes:
                    encrypted_quote_author_index = j
                    encrypted_quote = quotes_and_authors_braille_encrypted[j][0]
                    forward_slashes_matches = re.finditer("⠸⠌", encrypted_quote)
                    forward_slashes_match_indices = [match.start() for match in forward_slashes_matches]
                    quote_line_list = []
                    current_row_length = 0
                    for k in range(len(forward_slashes_match_indices)):
                        #If the forward slash space delimitor ("⠸⠌") under investigation
                        #is the last one in the "forward_slashes_match_indices" list,
                        #and the current line sublist within "quote_line_list" isn't the
                        #first one, and there is enough space in the current line to
                        #accomodate the sliced portion of the encrypted quote in-between
                        #the preceding "⠸⠌" delimitor (exclusively) and the end of
                        #the encrypted quote, that string is then added to the last
                        #element within the nested list "quote_line_list".
                        #The plus two after the slices are to entirely cover the "⠸⠌"
                        #delimitors, while the minus two after "number_of_columns" is
                        #to account for the vertical borders of box that will contain the quote
                        if (k == len(forward_slashes_match_indices)-1 and quote_line_list != [] and current_row_length +
                        len(encrypted_quote[forward_slashes_match_indices[k-1]+2:]) <= number_of_columns - 2):
                            word_string = (encrypted_quote[forward_slashes_match_indices[k-1] + 2:])
                            quote_line_list[-1][0] += word_string
                            current_row_length += len(word_string)
                        #If the forward slash space delimitor ("⠸⠌") under investigation
                        #is the last one in the "forward_slashes_match_indices" list,
                        #and the current line sublist within "quote_line_list" isn't the
                        #first one, and there is not enough space in the current line to
                        #accomodate the sliced portion of the encrypted quote in-between
                        #the preceding "⠸⠌" delimitor (exclusively) and the end of
                        #the encrypted quote, a list containing that string is then appended
                        #to the the nested list "quote_line_list" if its length is within
                        #the available space for a line.
                        #The plus two after the slices are to entirely cover the "⠸⠌"
                        #delimitors, while the minus two after "number_of_columns" is
                        #to account for the vertical borders of box that will contain the quote
                        elif (k == len(forward_slashes_match_indices)-1 and quote_line_list != [] and
                        (current_row_length + len(encrypted_quote[forward_slashes_match_indices[k-1]+2:]) >
                        number_of_columns - 2)):
                            word_string = (
                            encrypted_quote[forward_slashes_match_indices[k-1]+2:])
                            if len(word_string) < number_of_columns - 2:
                                quote_line_list.append([word_string])

                        #If the forward slash space delimitor ("⠸⠌") under investigation
                        #is not the first one in the "forward_slashes_match_indices" list,
                        #and the current line sublist within "quote_line_list" isn't the
                        #first one, and there is enough space in the current line to
                        #accomodate for the sliced portion of the encrypted quote
                        #in-between the preceding  "⠸⠌" delimitor (exclusively) and
                        #the current one (inclusively), then that string is added to
                        #the last element within the nested list "quote_line_list".
                        #The plus two after the slices are to entirely cover the "⠸⠌"
                        #delimitors, while the minus two after "number_of_columns" is
                        #to account for the vertical borders of box that will contain the quote
                        elif (k > 0 and quote_line_list != [] and current_row_length +
                        len(encrypted_quote[forward_slashes_match_indices[k-1] +
                        2:forward_slashes_match_indices[k] + 2]) <= number_of_columns - 2):
                            word_string = (encrypted_quote[forward_slashes_match_indices[k-1] +
                            2:forward_slashes_match_indices[k] + 2])
                            quote_line_list[-1][0] += word_string
                            current_row_length += len(word_string)

                        #If it is the first line being added to "quote_line_list" and
                        #that there is sufficient room in the line to add the beginning
                        #of the encrypted quote up to the delimitor under investigation,
                        #then these are added as the first sublist of "quote_line_list".
                        #"current_row_length" is incremented by the length of the string slice.
                        elif quote_line_list == [] and current_row_length <= number_of_columns - 2:
                            word_string = encrypted_quote[:forward_slashes_match_indices[k] + 2]
                            quote_line_list.append([word_string])
                            current_row_length += len(word_string)
                        #In other cases where there is not enough enough room in the current
                        #line to accomodate the quote slice between the last delimitor
                        #(exclusively) and the next one (inclusively) stored in the variable
                        #"word_string", a new line is started.
                        else:
                            word_string = (
                            encrypted_quote[forward_slashes_match_indices[k-1]+2:forward_slashes_match_indices[k]+2])
                            #If the "word_string" can fit on one line, it is appended to
                            #the list "quote_line_list". Otherwise, it is split along the delimitors
                            #("⠸⠌") in order to find the latest instance of a delimitor that would allow
                            #for both the truncated string "word_string_truncated" and the remainder of
                            #the original string after it was split "word_string_spillover"
                            #to both fit in their own line.
                            if len(word_string) < number_of_columns - 2:
                                quote_line_list.append([word_string])
                                #Here "current_row_length" is reset to the length
                                #of "word_string", as a new line has started.
                                current_row_length = len(word_string)
                            #If there isn't room in a new line for the entire "word_string",
                            #further "⠸⠌" word delimitors are found within "word_string"
                            #and it is split in order to fit in two lines.
                            else:
                                forward_slashes_matches_long_line = re.finditer("⠸⠌", word_string)
                                forward_slashes_match_indices_long_line = (
                                [match.start() for match in forward_slashes_matches_long_line])
                                #The loop proceeds in reverse order to find the first instance of the "⠸⠌"
                                #word delimitor (starting from the end of the line) that would allow to split
                                #the line, in order to avoid having a very short line followed by a line that
                                #is still too long.
                                for k in range(len(forward_slashes_match_indices_long_line)-1, -1, -1):
                                    word_string_truncated = word_string[:forward_slashes_match_indices_long_line[k] + 2]
                                    word_string_spillover = word_string[forward_slashes_match_indices_long_line[k]+ 2:]
                                    if (len(word_string_truncated) <= number_of_columns - 2 and
                                    len(word_string_spillover) <= number_of_columns - 2):
                                        quote_line_list.append([word_string_truncated])
                                        quote_line_list.append([word_string_spillover])


                    #If the "quote_line_list" populated using the encrypted quote found at the index j (or
                    #"encrypted_quote_author_index") of the "quotes_and_authors_braille_encrypted" list has a
                    #number of lines below a certain threshold, the index "j" is appended to the list "done_quotes",
                    #as the quote is suitable to be used to make a cryptogram. A "break" command exits the
                    #"for j in randomized_indices:" loop because a cryptogram candidate has already been found.
                    #The threshold depends on the specified "number_of_rows", minus the invariable amount of rows
                    #(two rows for the header and two rows for the box horizontal lines), divided by two (rounded down)
                    #to account for the fact that for every line of cryptogram, an additional empty line must be included
                    #to allow for the braille letter-labelled magnetic push pins to be placed on the embossed cryptogram.
                    if len(quote_line_list) <= (number_of_rows-4)//2 and len(quotes_and_authors_braille[j][0]) >= 80:
                        done_quotes.append(j)
                        break
                    #If the number of lines in "quote_line_list" is above the threshold, the index "j" is appended to
                    #the list "unacceptable_quotes", so that these indices are not considered in further rounds of the
                    #"for j in randomized_indices:" loop.
                    elif len(quote_line_list) > (number_of_rows-4)//2 or len(quotes_and_authors_braille[j][0]) < 80:
                        unacceptable_quotes.append(j)

            #The variable "current_row_length" will keep tabs of the
            #length of the line sublist being currently assembled
            #and will determine when to start a new line (new sublist)
            #in the "solution_rows" list. A list of individual braille
            #words forming the cryptogram solution is assembled by splitting
            #the string along spaces. In a similar approach as above, the
            #words will be added to the last sublist (designating the current
            #line) of "solution_rows", insofar as there is enough space left
            #for it plus an empty braille cell (as there will be no vertical box
            #borders for the solution, "+2" isn't added to "number_of_columns").
            current_row_length = 0
            solution_rows = []
            solution_words = quotes_and_authors_braille[encrypted_quote_author_index][0].split()
            for i in range(len(solution_words)):
                if solution_rows != [] and current_row_length + len(solution_words[i]) + 1 < number_of_columns:
                    solution_rows[-1] = [solution_rows[-1][0] + solution_words[i] + "⠀"]
                    current_row_length += len(solution_words[i]) + 1
                else:
                    solution_rows.append([solution_words[i] + "⠀"])
                    current_row_length = len(solution_words[i]) + 1

            #The author name is added if the user didn't provide some text of
            #their own instead of using the quote database.
            if user_text == []:
                author_name = "⠀⠠⠤⠀" + quotes_and_authors_braille[encrypted_quote_author_index][1].replace(" ", "⠀")
                #If the "author_name" string can fit on one line, it is appended to
                #the list "solution_rows". Otherwise, it is split along the spaces
                #(empty braille cells) in order to find the latest instance of a
                #space that would allow for both the truncated string "author_name_truncated"
                #and the remainder of the original string after it was split "author_name_spillover"
                #to both fit in their own line.
                if len(author_name) <= number_of_columns:
                    solution_rows.append([author_name])
                else:
                    empty_braille_cell_matches = re.finditer("⠀", author_name)
                    empty_braille_cell_match_indices = [match.start() for match in empty_braille_cell_matches]
                    for i in range(len(empty_braille_cell_match_indices)-1, -1, -1):
                        author_name_truncated = author_name[:i+1]
                        author_name_spillover = author_name[i+1:]
                        if (len(author_name_truncated) <= number_of_columns and
                        len(author_name_spillover) <= number_of_columns):
                            solution_rows.append([author_name_truncated])
                            solution_rows.append([author_name_spillover])

            #The function "validate_text()" determines if every character
            #within the "user_text[0]" string is a letter or a standard
            #punctuation mark. If so, it returns True. If not, it returns False.
            def validate_text(user_text):
                for char in user_text[0]:
                    if char.lower() not in ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ".", "!", "?",
                    ",", ";", ":", "-", "–", "—", "(", ")", "[", "]", "{", "}", "'", '"', "“", "”", "‘",
                    "’", "«", "»", "…"]:
                        return False
                    else:
                        return True
            #If the user has supplied some text as an additional argument ("user_text") and
            #that the number of lines (sublists) in the list "quote_line_list" is above the
            #threshold or the number of characters (including spaces) within the braille string
            #is below 80 characters, or if every character within the string isn't a letter or
            #standard punctuation mark, an error message is printed.
            if (user_text != [] and (len(quote_line_list) > number_of_rows-4//2 or
            len(quotes_and_authors_braille[encrypted_quote_author_index][0]) < 80 or
            validate_text(user_text) == False)):
                print("Your text needs to be at least 80 characters long (including spaces) and comprised of " +
                "letters and standard punctuation mark. The maximal length of your text depends on the number of" +
                "spaces and the specified number of rows and columns (defaulting to 25 rows and 32 columns). " +
                "Please try again with a revised text.")

            #If the "Crypto-Braille Cryptograms" folder doesn't already
            #exist in the working folder, it will be created.
            #Within it, the "Portable Embosser Format (PEF)" and
            #"Braille Ready Format (BRF)" subfolders will be created
            #as well, if not already present.
            if not os.path.exists(os.path.join(cwd, "Crypto-Braille Cryptograms", "Portable Embosser Format (PEF)")):
                os.makedirs(os.path.join(cwd, "Crypto-Braille Cryptograms", "Portable Embosser Format (PEF)"))
            if not os.path.exists(os.path.join(cwd, "Crypto-Braille Cryptograms", "Braille Ready Format (BRF)")):
                os.makedirs(os.path.join(cwd, "Crypto-Braille Cryptograms", "Braille Ready Format (BRF)"))

            #Compiles the list of Portable Embosser format (".pef") and Braille Ready Format (".brf") files
            #in the respective subfolder within the "Crypto-Braille Cryptograms" subfolder in the working folder.
            for _, dirnames, filenames in os.walk(os.path.join(cwd, "Crypto-Braille Cryptograms", "Portable Embosser Format (PEF)")):
                cryptogram_pef_files = [filename for filename in filenames if filename[-4:] == ".pef"]
            for _, dirnames, filenames in os.walk(os.path.join(cwd, "Crypto-Braille Cryptograms", "Braille Ready Format (BRF)")):
                cryptogram_brf_files = [filename for filename in filenames if filename[-4:] == ".brf"]

            #The digit of every file is extracted from its name and the maximum file number is determined for
            #the PEF and/or BRF files, if the "cryptogram_pef_files" and/or "cryptogram_brf_files" list isn't empty,
            #respectively. The starting splicing index of the "filename" corresponds to the index right after
            #the second hyphen ("Crypto-Braille Cryptogram number-"), and the filename is spliced up to the file extension,
            #exclusively.
            largest_cryptogram_pef_file_number = []
            largest_cryptogram_brf_file_number = []
            if cryptogram_pef_files != []:
                largest_cryptogram_pef_file_number = max([int(filename[33:-4]) for filename in cryptogram_pef_files])
            if cryptogram_brf_files != []:
                largest_cryptogram_brf_file_number = max([int(filename[33:-4]) for filename in cryptogram_brf_files])

            #If both lists "cryptogram_pef_files" and "cryptogram_brf_files" weren't empty,
            #then the maximum between "largest_cryptogram_pef_file_number" and "largest_cryptogram_brf_file_number"
            #is determined. If only one of "cryptogram_pef_files" or "cryptogram_brf_files"
            #wasn't empty, then the largest cryptogram file number for that file extension
            #is used as the "number_of_cryptogram_files" in order to pick up where the last
            #cryptogram problem was generated. If both "cryptogram_pef_files" and "cryptogram_brf_files"
            #are empty lists, "number_of_cryptogram_files" is initialized at zero.
            if cryptogram_pef_files != [] and cryptogram_brf_files != []:
                number_of_cryptogram_files = max(largest_cryptogram_pef_file_number, largest_cryptogram_brf_file_number)
            elif cryptogram_pef_files != [] and cryptogram_brf_files == []:
                number_of_cryptogram_files = largest_cryptogram_pef_file_number
            elif cryptogram_pef_files == [] and cryptogram_brf_files != []:
                number_of_cryptogram_files = largest_cryptogram_brf_file_number
            elif cryptogram_pef_files == [] and cryptogram_brf_files == []:
                number_of_cryptogram_files = 0

            #The dictionary "braille_numbers" is used to transcribe the string versions of "number_of_cryptogram_files"
            #and "total_number_of_empty_cells" into ASCII.
            braille_numbers = {"0":"⠚", "1":"⠁", "2":"⠃", "3":"⠉", "4":"⠙", "5":"⠑", "6":"⠋", "7":"⠛", "8":"⠓", "9":"⠊"}
            current_file_number = number_of_cryptogram_files + 1

            #The "current_file_number_braille" string is initialized with the braille numeric symbol "⠼",
            #and every braille digit equivalent of each character constituting the string version of
            #"current_file_number".
            current_file_number_braille = "⠼"
            for digit in str(current_file_number):
                current_file_number_braille += braille_numbers[digit]

            current_file_name = "Crypto-Braille cryptogram number-" + str(current_file_number)

            #PEF file is assembled by including opening and closing volume, section,
            #page and row tags, with the cryptogram puzzle, cipher and solution sandwitched
            #in between.
            pef_file_name = current_file_name +  ".pef"
            with open(os.path.join(cwd, "Crypto-Braille Cryptograms", "Portable Embosser Format (PEF)", pef_file_name), "a+", encoding="utf-8") as pef_file:
                pef_file.write('<?xml version="1.0" encoding="UTF-8"?>' +
                '\n<pef version="2008-1" xmlns="http://www.daisy.org/ns/2008/pef">\n\t<head>' +
                '\n\t\t<meta xmlns:dc="http://purl.org/dc/elements/1.1/">' +
            	'\n\t\t\t<dc:format>application/x-pef+xml</dc:format>' +
            	'\n\t\t\t<dc:identifier>org.pef-format.00002</dc:identifier>\n\t\t</meta>')

                pef_file.write('\n\t</head>\n\t<body>\n\t\t<volume cols="' + str(number_of_columns) + '" rows="'
                + str(number_of_rows) + '" rowgap="0" duplex="false">' +
                '\n\t\t\t<section>\n\t\t\t\t<page>\n\t\t\t\t\t<row>⠠⠉⠗⠽⠏⠞⠕⠤⠃⠗⠇</row>' +
                '\n\t\t\t\t\t<row>⠠⠉⠗⠽⠏⠞⠕⠛⠗⠁⠍⠀' + current_file_number_braille +
                '⠒</row>\n\t\t\t\t\t<row>' + (number_of_columns)*"⠤" + "</row>")
                #For each of the encrypted quote lines, the "spacing" variable is defined as
                #the number of empty braille cells required to complete the line up to the maximal
                #allowed width. Adding such a spacer will allow for the vertical box delimiters "⠸"
                #on the right side of every row to line up nicely.
                for i in range(len(quote_line_list)):
                    spacing = (number_of_columns-(len(quote_line_list[i][0])+2))*"⠀"
                    pef_file.write("\n\t\t\t\t\t<row>⠇" + (number_of_columns-2)*"⠀" + "⠸</row>")
                    pef_file.write("\n\t\t\t\t\t<row>⠇" + quote_line_list[i][0] + spacing + "⠸</row>")
                pef_file.write('\n\t\t\t\t\t<row>⠧' + (number_of_columns-2)*"⠤" + "⠼</row>")
                pef_file.write("\n\t\t\t\t</page>\n\t\t\t\t<page>\n\t\t\t\t\t<row>⠠⠉⠗⠽⠏⠞⠕⠤⠃⠗⠇</row>" +
                '\n\t\t\t\t\t<row>⠠⠉⠗⠽⠏⠞⠕⠛⠗⠁⠍⠀' + current_file_number_braille + "</row>\n\t\t\t\t\t" +
                "<row>⠠⠉⠊⠏⠓⠻⠒</row>\n\t\t\t\t\t<row>" + (number_of_columns)*"⠤" + "</row>")
                for i in range(len(cipher_list_of_lines)):
                    spacing = (number_of_columns-(len(cipher_list_of_lines[i][0])+2))*"⠀"
                    pef_file.write("\n\t\t\t\t\t<row>⠇" + cipher_list_of_lines[i][0] + spacing + "⠸</row>")
                pef_file.write('\n\t\t\t\t\t<row>⠧' + (number_of_columns-2)*"⠤" + "⠼" + "</row>" +
                "\n\t\t\t\t\t<row></row>\n\t\t\t\t\t<row>⠠⠎⠕⠇⠥⠰⠝⠀⠿⠀⠠⠏⠥⠵⠵⠇⠑⠀" + current_file_number_braille + "⠒</row>")
                for i in range(len(solution_rows)):
                    pef_file.write("\n\t\t\t\t\t<row>" + solution_rows[i][0] + "</row>")

                pef_file.write("\n\t\t\t\t</page>\n\t\t\t</section>\n\t\t</volume>\n\t</body>\n</pef>")

                #In this section the Braille Ready Format (BRF) files will be created.
                #The dictionary "ASCII_numbers" is used to transcribe the string versions of "number_of_cryptogram_files"
                #and "total_number_of_empty_cells" into ASCII.
                ASCII_numbers = {"0":"J", "1":"A", "2":"B", "3":"C", "4":"D", "5":"E", "6":"F", "7":"G", "8":"H", "9":"I"}

                #The "current_file_number_ASCII" string is initialized as the ASCII
                #equivalent of a numberic braille simbol ("#"), followed by every ASCII
                #equivalent of each braille character constituting the
                #string version of "current_file_number".
                current_file_number_ASCII = "#"
                for digit in str(current_file_number):
                    current_file_number_ASCII += ASCII_numbers[digit]

                BRL_to_ASCII = [["⠸⠌", "/"], ["⠠⠤","-"], ["⠐⠠⠤","-"], ["⠸⠦","8"], ["⠘⠦","8"], ["⠠⠶","8"], ["⠠⠦","'"],
                ["⠸⠴","8"], ["⠘⠴","8"], ["⠠⠴","'"], ["⠐⠣","7"], ["⠐⠜","7"], ["⠨⠣",""], ["⠨⠜",""], ["⠸⠣",""],
                ["⠸⠜",""], ["⠁","A"], ["⠃","B"], ["⠉","C"], ["⠙","D"], ["⠑","E"], ["⠋","F"], ["⠛","G"],
                ["⠓","H"], ["⠊","I"], ["⠚","J"], ["⠅","K"], ["⠇","L"], ["⠍","M"], ["⠝","N"], ["⠕","O"],
                ["⠏","P"], ["⠟","Q"], ["⠗","R"], ["⠎","S"], ["⠞","T"], ["⠥","U"], ["⠧","V"], ["⠺","W"],
                ["⠭","X"], ["⠽","Y"], ["⠵","Z"], ["⠂","1"], ["⠲","4"], ["⠒","3"], ["⠆","2"], ["⠤","-"],
                ["⠖","6"], ["⠦","8"], ["⠄","'"], ["⠀", " "]]

                #A BRF file is assembled here.
                brf_file_name = current_file_name + ".brf"
                with open(os.path.join(cwd, "Crypto-Braille Cryptograms", "Braille Ready Format (BRF)", brf_file_name), "a+") as brf_file:
                    brf_file.write(",CRYPTO-BRL")
                    brf_file.write("\n,CRYPTOGRAM " + current_file_number_ASCII + "3")
                    brf_file.write("\n" + (number_of_columns)*"-")
                #For each of the encrypted quote lines, the "spacing" variable is defined as
                #the number of empty braille cells required to complete the line up to the maximal
                #allowed width. Adding such a spacer will allow for the vertical box delimiters "_"
                #on the right side of every row to line up nicely. For every braille string in the
                #nested lists "quote_line_list", "cipher_list_of_lines" and "solution_rows",
                #the braille is converted to ASCII format ty performing a series of "re.sub()"
                #methods on them for each element of the "BRL_to_ASCII" list, starting with the
                #multi-character braille symbols to avoid any ambiguities. The square and curly bracket
                #braille symbols are converted to empty strings, as there is no equivalent in ASCII format:
                #(["⠨⠣",""], ["⠨⠜",""], ["⠸⠣",""],["⠸⠜",""]). The em- and en-dash are both converted
                #to a hyphen, as there is no ASCII version for these braille symbols: (["⠠⠤","-"], ["⠐⠠⠤","-"]).
                    for i in range(len(quote_line_list)):
                        brf_file.write("\nL" + (number_of_columns-2)*" " + "_")
                        ASCII_line = quote_line_list[i][0]
                        for j in range(len(BRL_to_ASCII)):
                            ASCII_line = re.sub(BRL_to_ASCII[j][0], BRL_to_ASCII[j][1], ASCII_line)
                        #The spacing variable needs to be defined after converting the
                        #braille characters into ASCII, as some of the braille symbols
                        #have multiple characters mapping to a single ASCII character
                        #(em- and en-dash converted into hyphens "["⠠⠤","-"], ["⠐⠠⠤","-"]"),
                        #while the curly and square brackets are removed altogether
                        #(["⠨⠣",""], ["⠨⠜",""], ["⠸⠣",""],["⠸⠜",""]).
                        spacing = (number_of_columns-(len(ASCII_line)+2))*" "
                        brf_file.write("\nL" + ASCII_line + spacing + "_")
                    brf_file.write("\nV" + (number_of_columns-2)*"-" + "#")

                    brf_file.write("\f,CRYPTO-BRL")
                    brf_file.write("\n,CRYPTOGRAM " + current_file_number_ASCII)
                    brf_file.write("\n,CIPH]3")
                    brf_file.write("\n" + (number_of_columns)*"-")

                    for i in range(len(cipher_list_of_lines)):
                        ASCII_line = cipher_list_of_lines[i][0]
                        for j in range(len(BRL_to_ASCII)):
                            ASCII_line = re.sub(BRL_to_ASCII[j][0], BRL_to_ASCII[j][1], ASCII_line)
                        spacing = (number_of_columns-(len(ASCII_line)+2))*" "
                        brf_file.write("\nL" + ASCII_line + spacing + "_")
                    brf_file.write("\nV" + (number_of_columns-2)*"-" + "#")

                    brf_file.write("\n\n,SOLU;N = ,PUZZLE " + current_file_number_ASCII + "3")
                    for i in range(len(solution_rows)):
                        ASCII_line = solution_rows[i][0]
                        for j in range(len(BRL_to_ASCII)):
                            ASCII_line = re.sub(BRL_to_ASCII[j][0], BRL_to_ASCII[j][1], ASCII_line)
                        brf_file.write("\n" + ASCII_line)
                bar()

if number_of_cryptograms == 1 and len(hint_list) == 1:
    print('\nThe BRF and PEF files "' + current_file_name +
    '" containing ' + str(len(hint_list)) + ' hint were created successfully!\n')
elif number_of_cryptograms == 1 and len(hint_list) != 1:
    print('\nThe BRF and PEF files "' + current_file_name +
    '" containing ' + str(len(hint_list)) + ' hints were created successfully!\n')
elif number_of_cryptograms > 1:
    print('\nYour ' + str(number_of_cryptograms) +
    ' cryptogram puzzles have been created successfully!')
