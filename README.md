# stego_python
short scripts for hiding text at pictures. 
Run these with use of python console

# usage:
<code>
encode.py -p picture -t text
</code>

Where <i>picture</i> is a file inside of which message from <i>text</i> file will be hidden.

Output from this script is a <b>encrypted.png</b> file

<code>
decode.py -p picture -t text
</code>

Where <i>picture</i> is a file with encoded message and <i>text</i> is output file for message.

<code>
stego.py -p picture -t text -m mode
</code>

Combined script. 

<i>mode</i> parameter decides about type of operation: <b>encode</b> writes text into picture and <b>decode</b> extract message from picture file.

