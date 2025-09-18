# CLai

## <u>C</u>ommand <u>L</u>ine <u>AI</u>

___Console program to converse with Gpt OpenAI Completion engine___ 

This is an uncomplicated console AI conversation utility for Linux and Windows.

(CLai == _clay_)  

    usage: python3 clai.py
    [PROMPT | log | clear | new | purge | model {model} | system {system message...}]

| command line | purpose             |
| :--- | :---                        |
|`clai PROMPT...`                    |write the prompt on the command line  
|`clai log      `                    |print out the log contents to the console  
|`clai new      `                    |new conversation for current directory  
|`clai clea[r\|n]`                   |erase `.clai_local` directory and all it's files  
|`clai purge\|del    `                |erase log file  
|`clai model {model}`                |set model for current directory  
|`clai system {"system prompt text"}`|set system prompt  

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

In your `.bashrc` file  
for example: `export GPTMOD=gpt-4o-mini`

