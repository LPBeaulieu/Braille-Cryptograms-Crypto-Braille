# Crypto-Braille
This application generates virtually unlimited famous quote cryptograms in PEF and BRF format! 
![Crypto-Braille in Action!](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille/blob/main/Crypto-Braille%20Thumbnail.jpg)
<h3 align="center">Crypto-Braille</h3>
<div align="center">
  
  [![License: AGPL-3.0](https://img.shields.io/badge/License-AGPLv3.0-brightgreen.svg)](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille/blob/main/LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/LPBeaulieu/Braille-Cryptograms-Crypto-Braille)](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille)
[![GitHub issues](https://img.shields.io/github/issues/LPBeaulieu/Braille-Cryptograms-Crypto-Braille)](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
  
</div>

---

<p align="left"> <b>Crypto-Braille</b> is an app that generates braille cryptograms based on famous quotes, in Portable Embosser Format (PEF) and Braille Ready Format (BRF). It also allows you to enter some text to generate your very own cryptograms!

The image above shows how you could play directly on embossed cryptogram puzzles, with the help of braille-labelled magnetic push pins. I recommend laying a placemat over the metallic magnetic board in order to decrease the strength of the neodymium-based magnets, which could otherwise crush the braille dots. Also, the base diameter of the magnets should be at most 15 mm (or 0.6 in) in order to properly fit within the designated spaces of the embossed cryptogram and cipher. Even then, the magnets need to be staggered in the cipher box as shown in the image above, so that all of the letters can have their corresponding encrypted magnetic label in place within the cipher box. As I don't have access to a braille embosser, I typed my cryptogram on my Perkins Brailler, but it should print very nicely in portrait mode on 8 1/2 by 11" braille or cardstock paper.</p> 
<p>As a sidenote, the quote in the image above reads "<i>It requires wisdom to understand wisdom: the music is nothing if the audience is deaf. — Walter Lippmann</i>".<br><br>
</p>

## 📝 Table of Contents
- [Dependencies / Limitations](#limitations)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## ⛓️ Dependencies / Limitations <a name = "limitations"></a>
- The cryptogram puzzles are generated on two pages, the first of which contains the encrypted text within an embossed box. <b>Each character of a word is separated by an empty braille cell, and each word is delimited by a forward slash ("⠸⠌") braille symbol in the PEF files or "st" character ("⠌") in the BRF files</b>. The second page is comprised of the cipher, also in an embossed box, followed by the solution. 
- Users can choose to <b>enter their own text instead of using the random quotes</b> that Crypto-Braille outputs by default. If that is the case, then the text should be <b>at least eighty characters in length (including spaces)</b> in order to provide the player with enough words to solve the cryptogram. The maximum length for the text is determined by the number of spaces present in it and the specified number of columns per line.
- The number of columns per line and rows per page are set by default to 30 and 25, respectively. These parameters may be tuned by the user according to the braille embosser's specifications. However, in order to have a more convenient and smaller playing area when laying both pages side by side, as depicted in the image above, <b>printing in portrait mode on either A4 or letter paper is recommended</b>.
- The random quotes selected from the "Quotable" database are chosen in such a way that their encrypted version will properly fit within a page. As such, the number of different quotes that can be converted into cryptograms using distinct ciphers at any one time will depend on the specified number of rows and columns, with longer quotes being included with wider and more numerous rows. Even so, it should be possible to  simultaneously generate over 100 individual encrypted quotes (each separate quote having a different cipher) with the margins set for printing on A4 paper.



## 🏁 Getting Started <a name = "getting_started"></a>

The following instructions will be provided in great detail, as they are intended for a broad audience and will
allow to run a copy of <b>Crypto-Braille</b> on a local computer. Here is a link to an instructional video explaining the steps described below: **The link will be added once the Youtube video is posted.**

The steps below are given for Linux operating system (OS) environments, as I work with Linux on my computer, but the code should run fine on other operating systems (windows, macOS) as well. Please send me an e-mail to the address below should you encounter any issues and I will try to further improve my code.

<b>Step 1</b>- Head over to the main <b>Crypto-Braille</b> github page, click on the <b>Code</b> button and then click on the <b>Download zip</b> button.
Extract the zipped folder into your desired location, and the "Braille-Cryptograms-Crypto-Braille-main" folder will now serve as your working folder, which contains the Python code you will later run in order to generate cryptogram puzzles.   

![Download Code Screenshot](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille/blob/main/Download%20Folder%20Illustration.svg)<hr>
<b>Figure 2</b>:The image above shows the steps to take in order to download the compressed folder containing the code.<br><br>

<b>Step 2</b>- In order to set up <b>Crypto-Braille</b> on your computer, access your working folder in the file explorer, and click on the folder’s arrow in the window’s header. Then, simply click on "open in terminal" in order to open a windowed command line, with a correct path to your working folder, as shown in Figure 3.

![Open in Terminal Screenshot](https://github.com/LPBeaulieu/Braille-Cryptograms-Crypto-Braille/blob/main/Open%20in%20Terminal%20Illustration.svg)<hr>
<b>Figure 3</b>: The image above shows the steps to take in order to open the command line in your working folder.<br><br>

 Copy and paste (or write down) the following in the command line to install <b>alive-Progress</b> (Python module for a progress bar displayed in command line): 
```
pip install alive-progress
```

<b>Step 3</b>- You're now ready to use <b>Crypto-Braille</b>! 🎉

## 🎈 Usage <a name="usage"></a>
To run the "crypto-braille.py" Python code, open a windowed command line in your working folder by entering the following:                
```              
python3 crypto-braille.py
```

Furthermore, you can have Crypto-Braille generate multiple braille cryptogram files (each containing one cryptogram and the cipher and solution on the following page) which are numbered for easy reference, by typing the desired number of cryptograms as a separate argument when running the Python code. For example, to generate 50 cryptograms with the default number of columns and rows of 30 and 25, respectively, you would enter the following in command line:
```              
python3 crypto-braille.py 50
```

In order to specify a different number of rows or columns, simply enter the desired number, directly preceded by "row" for rows or "col" for columns. For example, to generate a cryptogram with 40 columns and 25 rows, you would enter the following in command line. The order of the arguments does not matter, but please make sure to include a space in between the Python code file name and any supplemental arguments: 
```              
python3 crypto-braille.py col40 row25
```

Should you want to be given some hints in the form of cipher values for given letters, simply enter the requested letters as additional arguments. For example, should you like to know what the encrypted letters standing for "a" and "e" are, you would type the following:
```              
python3 crypto-braille.py a e
```

Should you want to have the identity of all 26 encrypted letters revealed to you in the cipher, simply add "hints26" as an supplemental argument when calling the Python code:
```              
python3 crypto-braille.py hints26
```

Should you like to submit your own text for encryption instead of a random quote, simply enter the text in quotes as a additional argument. Please note that the text should consist of at least eighty characters to enable players to readily decipher the code. Also, the text should only be made up of letters and standard punctuation marks. Only one cryptogram can be generated at a time when entering your own text, as in the example below:
```              
python3 crypto-braille.py "My text (at least eighty characters in length)".
```

Finally, any number of the abovementioned arguments can be combined in any order when calling the Python code. For example, should you like to generate 50 cryptograms with a number of columns and rows of 40 and 25, respectively, and having the "a" and "e" hints included in the ciphers, you would enter the following in command line:
```
python3 crypto-braille.py 50 col40 row25 a e
```

 <br><b>And that's it!</b> You're now ready to solve as many braille cryptograms as you like! If you are close to someone who is visually impaired and would like to help them find an accessible version of cryptogram puzzles, or maybe if you are only sprucing up your braille reading skills in preparation for the Zombie Apocalypse (lol) then this app is for you! P.S. be sure to also check out my other github page <b>e-Braille Tales</b> (https://github.com/LPBeaulieu/Braille-OCR-e-Braille-Tales) for braille OCR!🎉📖
  
  
## ✍️ Authors <a name = "author"></a>
- 👋 Hi, I’m Louis-Philippe!
- 👀 I’m interested in natural language processing (NLP) and anything to do with words, really! 📝
- 🌱 I’m currently reading about deep learning (and reviewing the underlying math involved in coding such applications 🧮😕)
- 📫 How to reach me: By e-mail! LPBeaulieu@gmail.com 💻


## 🎉 Acknowledgments <a name = "acknowledgments"></a>
- Hat tip to [@kylelobo](https://github.com/kylelobo) for the GitHub README template!




<!---
LPBeaulieu/LPBeaulieu is a ✨ special ✨ repository because its `README.md` (this file) appears on your GitHub profile.
You can click the Preview link to take a look at your changes.
--->
