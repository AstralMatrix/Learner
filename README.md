# Learner

Version 0.1.0

## Description

I wrote a program to help users to learn course material, or just material in general.

I found that I learn best through repetition. Although none of the flashcard-like programs that I came across really did it for me, and it always seemed like a pain to enter all of the material into them.

This inspired me to create the Learner. I wanted a way to quickly quiz myself on questions, while automatically verifying that I got it right. While also wanting a way to enter the material through a simple text editor.

I personally use this mainly to aide in language learning, but it can be used to help you learn / study / review any kind of topic, just like with flashcards.

## Requirements
- python3
- python3-tkinter

If you don't have `python3` installed, it can be found here: https://www.python.org/downloads/

This program does not use any `pip` packages, but does require `tkinter`. This comes with python by default, but may need a special installation in some cases. You can check if you already have it by opening a Python terminal and running `import tkinter`, if you get no errors then you are all set.

To install `tkinter` on debian you can run:

```console
sudo apt install python3-tk
```
In other cases, please refer to your package manager.

# How to Run

To get and run the Learner program, run:

```console
$ git clone https://github.com/AstralMatrix/Learner.git
$ cd Learner/src
$ python3 main.pyw
```

alternatively, you can click `Code`, then `Download ZIP`, then extract the zip file. To run, go to the `Learner` directory, then the `src` directory, and click on `main.pyw`. The GUI should now show up if `python3` and `tkinter` are installed properly, if nothing happens please refer to the `log.txt` file that will be created in the `src` directory.

## How to Make Data Files

Please refer to the [README.md](data/README.md) in `./data`

## Settings

- Active Box:
  - Files in the directory that will be used to be quizzed on.
- Disabled Box:
  - Files in the directory that will not be used.
- Directory:
  - The directory in which to look for data / quiz files.
- Font Size: 
  - The font size of the questions and answers being displayed.
- Typeface:
  - The font used.
- Theme:
  - The theme used. More themes can be defined in [settings.json](src/settings.json)
- Display Item:
  - The segment of the "quiz element" to be displayed, use -1 for random segments.

## Errors / Warnings

If an error or warning occurs, a message box is displayed, and it is logged in `./src/log.txt`.
- Warnings titled as `warning` in a message box or logged as `---Logging warning---` are caused by the user, and should be able to be fixed relatively easily. 
  - i.e. trying to load an invalid file, malformed json file, invalid modification to settings file, etc...
- Errors titled as `unhandled exception` in a message box or logged as `---Logging unhandled exception---` are issues within the code itself and are accompanied with a traceback.
  - Please create a new issue for help fixing these. In the issue, please include: python version, the error from `log.txt`, and a detailed description of what you were doing at the time that lead up to the error.

## Screenshots

**Quiz:**

![Example](https://user-images.githubusercontent.com/25624496/101077283-a1add500-3572-11eb-98c4-99c92a5c47b7.gif)

**Settings:**

![Settings_Form](https://user-images.githubusercontent.com/25624496/100784846-cde41d00-33dd-11eb-8108-f0a01854315f.png)

## License

This program is provided under the [GPL v3 License](LICENSE)
