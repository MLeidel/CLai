# CLai

## <u>C</u>ommand <u>L</u>ine <u>AI</u>

___Console program to converse with Gpt OpenAI Completion engine___ 

This is an uncomplicated console AI conversation utility for Linux and Windows.

LocalGem is a guided AI conversation utility that you run in a terminal.  
It is not an agentic coding assistant.

### Command Line AI

(CLai == `clay`)

    USAGE: python3 clai.py
      [PROMPT | log | clear | purge | list | 
       model {model} | new [role] ]
   
Running clai in a directory not previously visited,  
clai will assume a new conversation. Aside from the AI prompt,
clai has other commands to; view the log, start a new conversation,
completely clear the .clai_local directory, purge the log file,
switch to a different model (for this directory), display help.

| command line | purpose             |
| :--- | :---                        |
|`clai PROMPT...`                    |write the prompt on the command line  
|`clai log      `                    |print out the log contents to the console  
|`clai new [role]`                   |new conversation & optional new instructions 
|`clai clea[r\|n]`                   |erase .clai_local directory and all it's files  
|`clai purge    `                    |erase log file  
|`clai model {model}`                |set model for current directory  
|`clai list`                         |list all current OpenAI models  
|`clai help`                         |print out further help info  

---

### Directory level files

On running clai commands in a directory clai will continue a previous
conversation if detected.

Hiden file structure per visited directory:

    .clai_local/
        clai_conversation
        clai_model
        clai_log
        clai_sysmsg

---

clai requires these environment keys:

'GPTKEY' for openai key,  
'GPTMOD' for default openai model,  
'GPTMSG' for default system message  

for example: `export GPTMOD=gpt-4o-mini`

Hopefully you can find ways to execute clai.py.  

* `python3 clai.py [prompt or commands]`
* `python3 -m py_compile clai.py`
* `pyinstaller --onedir --clean --noconfirm --strip --contents-directory clai_files clai.py`
