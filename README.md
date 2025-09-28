# CLai

## <u>C</u>ommand <u>L</u>ine <u>AI</u>

___Console program to converse with Gpt OpenAI Completion engine___ 

This is an uncomplicated console AI conversation utility for Linux and Windows.

### Command Line AI

(CLai == `clay`)

    USAGE: python3 clai.py
      [PROMPT | log | clear | purge |  
       model {model} | new [role] ]
   
On running clai in a directory not previously visited,  
clai will prompt for model and assume new conversation.

| command line | purpose             |
| :--- | :---                        |
|`clai PROMPT...`                    |write the prompt on the command line  
|`clai log      `                    |print out the log contents to the console  
|`clai new [role]`                   |new conversation & optional new role  
|`clai clea[r\|n]`                   |erase .clai_local directory and all it's files  
|`clai purge    `                    |erase log file  
|`clai model {model}`                |set model for current directory  

On running clai in a directory not previously visited,  
clai will prompt for model and assume new conversation.

Files created:

    .clai_local/
        clai_conversation
        clai_model
        clai_log
        clai_sysmsg

clai requires these environment keys:

'GPTKEY' for openai key,  
'GPTMOD' for default openai model,  
'GPTMSG' for default system message  

for example: `export GPTMOD=gpt-4o-mini`

`pyinstaller --onedir --clean --noconfirm --strip --contents-directory clai_files clai.py`

