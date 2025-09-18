'''
clai.py
Command Line AI
(CLai == `clay`)

usage: clai [prompt | log | new | clear | purge | model {model} | system {system message...}]

Besides the prompt itself, other commands are:

  log       print out the log contents to the console
  new       new conversation for current directory
  clea[r|n] erase clai_conversation, clai_model, clai_log, clai_sysmsg
  purge     erase log clai_log
  model     set model for current directory
  system    set system message for current directory
  help      print clai help to console

On running clai in a directory not previously visited,
clai will prompt for model and assume new conversation

Files created:
    .clai_local/ clai_conversation, clai_model, clai_log, clai_sysmsg

Requires ENV keys:
'GPTKEY' for your openai key,
'GPTMOD' for default openai model,
'GPTMSG' for default system message
for example: export GPTMOD=gpt-4o-mini

pyinstaller --onedir --clean --noconfirm --strip --contents-directory clai_files clai.py
'''
import sys, os
from pathlib import Path
import datetime
import json
from time import localtime, strftime
from termcolor import cprint
from openai import OpenAI

MODEL = ""
SYSMSG = ""
now = datetime.datetime.now()

openmsg = '''
   _____   _                _
  / ____| | |              (_)
 | |      | |        __ _   _
 | |      | |       / _` | | |
 | |____  | |____  | (_| | | |
  \_____| |______|  \__,_| |_|

    Welcome to CLai `clay`

required environment variables:
'GPTKEY' OpenAI Auth Code
'GPTMOD' default model to use
'GPTMSG' default system message

Usage:
clai prompt...  launch your query to AI
clai log        print out log contents to the console
clai new        new conversation for current directory
clai clea[r|n]  erase .clai_local directory and all it's files
clai purge|del  erase log file
clai model {model} set model for current directory
clai system {"system prompt text"}  set system prompt
'''

helpmsg = '''
----------- c l a i  H E L P -----------
Command Line AI
(CLai == `clay`)
Install clai and clai_files in your system path

usage: clai
  [PROMPT... | log | html |
   clear | purge |
   model {model} |
   system {system message...}]

clai PROMPT...  write the prompt on command line
clai log        print out log contents to the console
clai new        new conversation for current directory
clai clea[r|n]  erase .clai_local directory and all it's files
clai purge|del  erase log file
clai model {model} set model for current directory
clai system {"system prompt text"}  set system prompt

On running clai in a directory not previously visited,
clai will prompt for model and assume new conversation.

Files created:
    .clai_local/
        clai_conversation
        clai_model
        clai_log
        clai_sysmsg

clai requires these environment keys:
'GPTKEY' for your openai key,
'GPTMOD' for default openai model,
'GPTMSG' for default system message
for example: export GPTMOD=gpt-4o-mini
'''

# FUNCTIONS

def error_abort(msg):
    cprint(f"{msg}\n", 'red', attrs=['bold',])
    sys.exit()

def load_buffer():
    try:
        with open(conversation_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # corrupted file -> start clean
        return []

def save_buffer(buf):
    with open(conversation_path, "w", encoding="utf-8") as f:
        json.dump(buf, f, ensure_ascii=False, indent=2)

def extract_token_counts(resp):
    """
    Return (total_tokens, prompt_tokens, completion_tokens)
    Works for both dict-like and object-like resp.
    """
    total_tokens = prompt_tokens = completion_tokens = None

    if isinstance(resp, dict):
        usage = resp.get('usage', {})
        total_tokens = usage.get('total_tokens')
        prompt_tokens = usage.get('prompt_tokens')
        completion_tokens = usage.get('completion_tokens')
    else:
        usage = getattr(resp, 'usage', None)
        if usage is not None:
            total_tokens = getattr(usage, 'total_tokens', None)
            prompt_tokens = getattr(usage, 'prompt_tokens', None)
            completion_tokens = getattr(usage, 'completion_tokens', None)

    return total_tokens, prompt_tokens, completion_tokens


def gptCode(key: str, model: str, messages: str) -> str:
    """Call the OpenAI ChatCompletion endpoint."""
    try:
        client = OpenAI(api_key=os.environ.get(key))
        resp = client.chat.completions.create(
        model    = model,
        messages = messages)
        content = resp.choices[0].message.content.strip()
        total_tokens, prompt_tokens, completion_tokens = extract_token_counts(resp)
        # Return as a tuple (content, total, prompt, completion)
        return content, total_tokens, prompt_tokens, completion_tokens
    except Exception as e:
        error_abort("Client Error " + str(e))
        return ""

# BEGIN PROCESS REQUEST

# all local clai files stored in this directory
# all visits to any directory by clai will create this hidden sub-directory
files_path = ".clai_local"
os.makedirs(files_path, exist_ok=True)
# make file path variable for easier file management syntax
log_path = os.path.join(files_path, "clai_log")
conversation_path = os.path.join(files_path, "clai_conversation")
model_path = os.path.join(files_path, "clai_model")
sysmsg_path = os.path.join(files_path, "clai_sysmsg")

# SET THE CORRECT MODEL

if os.path.isfile(model_path) is False:
    # no model set for directory
    MODEL = os.environ.get("GPTMOD")
    if MODEL is None:
        print("\nNo default model found in ENV\nMust have default\n")
        sys.exit()
else:
    # open model set for this directory
    MODEL = open(model_path, encoding='utf-8').read().strip()

# SET THE CORRECT SYSTEM PROMPT

if os.path.isfile(sysmsg_path) is False:
    # no prompt set for directory
    SYSMSG = os.environ.get("GPTMSG")
    if SYSMSG is None:
        print("\nNo default system message found in ENV\nMust have default.\n")
        sys.exit()
else:
    # open model set for this directory
    SYSMSG = open(sysmsg_path, encoding='utf-8').read().strip()

if len(sys.argv) <= 1:
    cprint(openmsg, 'yellow', attrs=['bold',])  # , attrs=['reverse']
    cprint(f"Model: {MODEL}\n", 'yellow', attrs=['bold',])
    cprint(f"System Msg: {SYSMSG}\n", 'yellow', attrs=['bold',])
    sys.exit()

# execute other command or prompt ...

if sys.argv[1].lower() == "model":
    if len(sys.argv) != 3:
        cprint("missing model name argument !\n", 'red', attrs=['bold',])
        sys.exit()
    MODEL = sys.argv[2].strip()
    open(model_path, 'w', encoding='utf-8').write(MODEL)
    cprint(f"Model: {MODEL}\n", 'yellow', attrs=['bold',])
    sys.exit()
elif sys.argv[1].lower() == "new":
    if os.path.isfile(conversation_path):
        os.remove(conversation_path)
    cprint("New conversation\n", 'yellow', attrs=['bold',])
    sys.exit()
elif sys.argv[1].lower() == "log":
    if os.path.isfile(log_path):
        cprint(open(log_path, encoding='utf-8').read(), 'yellow')
    sys.exit()
elif sys.argv[1].lower() == "purge" or sys.argv[1].lower() == "del":
    if os.path.isfile(log_path):
        os.remove(log_path)
    cprint("log purged\n", 'yellow', attrs=['bold',])
    sys.exit()
elif sys.argv[1].lower().startswith("clea"):
    if os.path.isfile(conversation_path):
        os.remove(conversation_path)
    if os.path.isfile(log_path):
        os.remove(log_path)
    if os.path.isfile(model_path):
        os.remove(model_path)
    if os.path.isfile(sysmsg_path):
        os.remove(sysmsg_path)
    # now remove empty directory
    Path(files_path).rmdir()
    cprint("clai files removed\n", 'yellow', attrs=['bold',])
    sys.exit()
elif sys.argv[1].lower() == "system":
    if len(sys.argv) != 3:
        cprint("missing 'text..' system 'text..'\n", 'red', attrs=['bold',])
        sys.exit()
    SYSMSG = sys.argv[2].strip()
    open(sysmsg_path, 'w', encoding='utf-8').write(SYSMSG)
    cprint(f"System Message: {SYSMSG}\n", 'yellow', attrs=['bold',])
    sys.exit()
elif sys.argv[1].lower() == "help":
    cprint(helpmsg, 'grey', attrs=['bold',])  # , attrs=['reverse']
    cprint(f"Current Model: {MODEL}", 'grey', attrs=['bold',])
    cprint(f"Current System Msg: {SYSMSG}\n", 'grey', attrs=['bold',])
    sys.exit()


# process prompt

CBUFF = []

query = ' '.join(sys.argv[1:])

# 1) add the user message
if os.path.isfile(conversation_path) is True:
    CBUFF = load_buffer()
else:
    CBUFF = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

CBUFF.append(
    {"role": "user", "content": query}
)

# 2) call the chat completion
ai_text, total, prompt, completion = gptCode("GPTKEY", MODEL, CBUFF)

if ai_text == "":
    sys.exit()

# 3) add the assistant reply to history
CBUFF.append(
    {"role": "assistant", "content": ai_text}
)

# 4) show it
cprint("\n" + ai_text + "\n", "green")

# SAVE conversation to disk
save_buffer(CBUFF)

# append to log
today = strftime("%a %d %b %Y", localtime())
tm    = strftime("%H:%M", localtime())
with open(log_path, "a", encoding="utf-8") as fout:
    fout.write("\n\n=== Chat on %s %s ===\n\n" % (today, tm))
    fout.write(f"prompt:{prompt}, completion:{completion}, total:{total} \n\n")
    for msg in CBUFF:
        role = msg["role"]
        fout.write(f"{role.upper()}:\n{msg['content']}\n\n")
    fout.write("="*40 + "\n\n")
