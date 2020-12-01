# How to Make Data Files

Data files can be one of two types `.json` or `.sfmt`.

Two example files come in this directory (one of each type).

## What is a DataObject?

A DataObject is the container for a given item that you want to be quizzed on. Therefore, one DataObject represents one question (with corresponding answers).

A DataObject contains segments, each segment is a list of strings. Each segment represents equivalent parts of the question. For example: Chinese Translation, English Translation, Pinyin. Since each of these parts are equivalent. This is simply a way of splitting up questions into different parts, so you can be quizzed on one segment, and provide the other segments as answers.

Within each segment of a DataObject can be multiple strings. These strings each represent a variation of that part of the question. For example if the first segment is "What is my favorite ice cream" the second segment might be "Mint" and "Vanilla", since both are valid answers to the question.

## How Users are Quizzed

Users are quizzed by displaying a given segment of the current `DataObject` or "question". The user can then input any one part of the other segments as a correct answer. If the user enters the a part of the segment being displayed, this will also be marked as correct.

When grading the user's response all ASCII symbols, white-space, and capitalization are ignored, but all other ASCII characters and all Unicode characters must match. Here are some examples of of this formatting:

- Answer: "Mint"
  - Possible correct response: " mint $%(&@ -/ ))--/)$(&^"
  - Incorrect response: "m1nt"
  - Incorrect response: "mit"
  - Incorrect response: " "

- Answer: "To call (a friend)"
  - Possible correct response: "to call a friend"
  - Possible correct response: "tO cALL a fRIeND"
  - Possible correct response: "t oca ll a(fri end)"
  - Incorrect response: "to call"
  - Incorrect response: "to call friend"

- Answer: "你好"
  - Possible correct response: "你 好"
  - Possible correct response: "你好 ^#*$&"
  - Incorrect response: "你"
  - Incorrect response: "好"
  - Incorrect response: "你好吗"

## JSON Formatting

The JSON files contain a 3D list of strings. The outer most list, is the list that contains all of the `DataObjects`. Each `DataObject` is made up of a 2D list of strings. Therefore the second most set of lists represents any given `DataObject`. Then, the third most set of lists represents the given segments for that `DataObject`. Then each of those lists contain strings, representing the variations of that segment.

Here are the examples above formatted in JSON (note the parts beginning with `<--` are not part of the actual data, and are just there to label the different parts):

```json
[    <-- List containing DataObjects
    [    <-- List representing a DataObject.
        ["你好"],    <-- List representing a segment of a DataObject.
        ["hello"],
        ["nǐ hǎo", "ni3 hao3", "ni hao"]
    ],
    [
        ["What is my favorite ice cream?"],
        ["Mint", "Vanilla"]
    ]
]
```

## SFMT Formatting

SFMT is a custom format that stands for "Simple Format", which is meant to be a much simpler way of creating data files. This format, when loaded in, makes DataObjects the same way as the JSON files. Instead of lists denoting each `DataObject`, they are each denoted by a new line. In addition to this each segment is denoted by a `-` and each part of that segment is denoted with a `/`.

Here are the examples above formatted in SFMT (when loaded they will be interpreted the exact same as the JSON example above):

```sfmt
你好 - hello - nǐ hǎo / ni3 hao3 / ni hao
What is my favorite ice cream? - Mint / Vanilla
```

With this said, the symbols `-` and `/` can therefore not appear in your actual data, otherwise they will be interpreted literally. Therefore it would be interpreted differently if the second line said "What is my favorite ice-cream?" instead of "What is my favorite ice cream?"