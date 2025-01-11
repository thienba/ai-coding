- Prompt 1
  ```plaintext
  Act as teacher or expert and based on the content inside ==== create [number of questions] multiple choice questions with this information with each multiple choice question having the following format with [level of difficulty]:
  
  Question: Question 1
  A: Answer 1
  B: Answer 2
  C: Answer 3
  D: Answer 4

  Only the question and the options

  ===================
  [lesson content]
  ===================
  ```
- Prompt 2
  ```plaintext
  You are a genius writer.
  Based on the passage inside --- [analyze or write more] about [number of words] words with [tone of voice].
  ---------------------
  [content]
  ---------------------
  ```
- Prompt 3
  ```plaintext
  Extract the information about inside "". I need three points: good, bad, total and rating 
  Format:
    Review 1: 
      Content: Content  comment
      Result: Bad or good
      Rating: Rating number
    => Sumarize: [number of good] good, [number of bad] bad, [total number of review] total, [average rating] rating

    "
      [list of review]
    "  
  ```
- Prompt 4
  ```plaintext
  Extract code from inside ==== in [language, framework or library], [find error, write content or explain code]. First, you can read the whole code. Then you need to write the code yourself, compare and give the [error, content or explanation] result.

  ===================
  [code]
  ===================
  ```
- Prompt 5
  ```plaintext
  Extract from the list of tourist attractions inside -----, introduce specific places, activities, famous dishes and attach the visiting time.
  First, you need to find that place. Then you can find some places according to that place

  ---------------------
  - Phu Quoc
  - Ho Chi Minh
  - Da Nang
  - [more places]
  ---------------------
  ```
- Prompt 6
  ```plaintext
  Extract information from this book. I need a brief of the book's content and a list of characters that appear in the book.
  
  [File]
  ```
