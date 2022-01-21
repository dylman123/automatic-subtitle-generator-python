# Example
Created by Dylan Klein

## Input video
A video is required to run the demo. The following file formats are supported:
- *.m4v
- *.mp4"
- *.mov"

For example, the video clip `input.m4v` was used as an input:
![Input Video](thumbnail.png)

## Captions CSV
A CSV file is generated automatically so that the user can edit captions after the Speech-To-Text transcription took place. Once edited, the CSV file is then converted into a FCPXML file.

For example, the file `captions.csv` was generated.

| Start (secs) | End (secs) | Duration (secs) | Captions | Speaker |
| ------------ | ---------- | --------------- | -------- | ------- |
| 0 | 1.5 | 1.5 | I'm fucking competitive | 2 |
| 1.6 | 2 | 0.4 | okay | 2 |
| 2.1 | 2.8 | 0.7 | don't get me started | 2 |
| 2.8 | 3.2 | 0.4 | like | 1 |
| 3.3 | 4.6 | 1.3 | what do you most competitive in | 1 |
| 5.8 | 7.4 | 1.6 | like if someone was like walking next | 2 |
| 7.4 | 8.7 | 1.3 | to me and they're like a little | 2 |
| 8.7 | 10.9 | 2.2 | like a stepfather I'll be like | 2 |
| 11 | 12.3 | 1.3 | fuck you I'm gonna beat ya you | 2 |
| 12.3 | 13.1 | 0.799999999999999 | gotta work fast | 2 |
| 13.2 | 13.7 | 0.5 | oh Mike | 2 |
| 14.8 | 16.4 | 1.6 | you're behind me if it's a friend | 2 |
| 16.4 | 16.9 | 0.5 | of mine | 2 |
| 17.6 | 19.2 | 1.6 | yeah let them waiting right if it's | 2 |
| 19.2 | 20.6 | 1.4 | a stranger I'm that we got | 2 |
| 20.9 | 22.3 | 1.4 | this gon go down | 2 |
| 22.5 | 23.8 | 1.3 | we're going Fight | 2 |
| 24.2 | 25.5 | 1.3 | You Gotta Have you ever gotten into | 1 |
| 25.5 | 26 | 0.5 | a fight | 1 |
| 27.7 | 28.3 | 0.600000000000001 | no | 2 |
| 28.5 | 28.8 | 0.300000000000001 | that's a | 2 |
| 28.8 | 29.5 | 0.699999999999999 | lie | 1 |
| 30.5 | 32 | 1.5 | who pauses for 10 seconds | 1 |
| 34.2 | 34.6 | 0.399999999999999 | well I'm from | 1 |
| 34.6 | 35.4 | 0.799999999999997 | Hobart | 2 |
| 36.2 | 38.2 | 2 | organ Central is until you've been to | 2 |
| 38.2 | 38.7 | 0.5 | her but | 2 |
| 38.8 | 40.4 | 1.6 | I just thought everybody is related to | 1 |
| 40.4 | 41.1 | 0.700000000000003 | everybody there | 1 |

## Output FCPXML
The outputted file is of the format .fcpxml and is readable by Final Cut Pro X. This allows the user to edit the auto-generated captions before the video is to be rendered.

For example, the file `output.fcpxml` was outputted. The following is an excerpt from `output.xml`:

```
...
<title duration="4500/3000s" lane="1" name="I'm fucking competitive - Basic Title" offset="236923687/30000s" ref="r6">
    <param key="9999/999166631/999166633/1/100/101" name="Position" value="-502.0 -330.0"/>
    <param key="9999/999166631/999166633/2/351" name="Flatten" value="1"/>
    <param key="9999/999166631/999166633/2/354/999169573/401" name="Alignment" value="1 (Center)"/>
    <text>
        <text-style ref="ts1">I'm fucking competitive</text-style>
    </text>
    <text-style-def id="ts1">
        <text-style alignment="center" bold="1" font="Futura" fontColor="1 1 1 1" fontFace="Condensed ExtraBold" fontSize="60" strokeColor="0 0 0 1" strokeWidth="3"/>
    </text-style-def>
</title>
<title duration="2400/3000s" lane="1" name="okay don't get me - Basic Title" offset="236971735/30000s" ref="r6">
    <param key="9999/999166631/999166633/1/100/101" name="Position" value="-502.0 -330.0"/>
    <param key="9999/999166631/999166633/2/351" name="Flatten" value="1"/>
    <param key="9999/999166631/999166633/2/354/999169573/401" name="Alignment" value="1 (Center)"/>
    <text>
        <text-style ref="ts2">okay don't get me</text-style>
    </text>
    <text-style-def id="ts2">
        <text-style alignment="center" bold="1" font="Futura" fontColor="1 1 1 1" fontFace="Condensed ExtraBold" fontSize="60" strokeColor="0 0 0 1" strokeWidth="3"/>
    </text-style-def>
</title>
<title duration="2400/3000s" lane="1" name="started like - Basic Title" offset="236995759/30000s" ref="r6">
    <param key="9999/999166631/999166633/1/100/101" name="Position" value="-502.0 -330.0"/>
    <param key="9999/999166631/999166633/2/351" name="Flatten" value="1"/>
    <param key="9999/999166631/999166633/2/354/999169573/401" name="Alignment" value="1 (Center)"/>
    <text>
        <text-style ref="ts3">started like</text-style>
    </text>
    <text-style-def id="ts3">
        <text-style alignment="center" bold="1" font="Futura" fontColor="1 1 1 1" fontFace="Condensed ExtraBold" fontSize="60" strokeColor="0 0 0 1" strokeWidth="3"/>
    </text-style-def>
</title>
...
```