# TTS Alerts And Chat

TTS Alerts And Chat is a Streamlabs Chatbot script that provides text-to-speech capabilities for Streamlabs alerts, chat messages, and a customizable command.

The text-to-speech uses your computer's narrator voice and has some customization for voice, volume, and speech rate.

Feel free to reach out to me in the [Streamlabs Chatbot discord](https://discord.gg/xFcsxft) (@Kruiser8) or on Twitter ([@Kruiser8](https://twitter.com/kruiser8)) with any questions or feedback.

# Credits

Thanks to [Ocgineer](https://github.com/ocgineer) for his [Streamlabs Event Receiver](https://github.com/ocgineer/Streamlabs-Events-Receiver) that allows events to be caught in a Streamlabs Chatbot script.

# Installation

For chatbot script installation help, please view this guide:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Prepare-&-Import-Scripts

For setting up the text-to-speech overlay:
https://github.com/StreamlabsSupport/Streamlabs-Chatbot/wiki/Script-overlays

# Usage

Before the alert text-to-speech will work, you'll need to add a Streamlabs Socket API token.

- In Streamlabs Chatbot, open the *Scripts* tab
- Click the *TTS Alerts And Chat* script in order to open the settings sidebar
- At the bottom, select the **Streamlabs Token** dropdown
- Click the *Get Socket Token* button or go to https://streamlabs.com/dashboard#/settings/api-settings in a browser.
- In the browser, click the **API Tokens** tab
- Copy the **Your Socket API Token**
- Paste this value into the **Streamlabs Socket Token** setting in the chatbot
- Click the *Save Settings* button at the bottom of the script settings

***

# Setting Information

All settings have extra information if you hover over the field in the chatbot. Below is a summarized list of settings.

## Text-To-Speech Settings
All TTS Voice settings are in this section.

### Voice Name
Set the narrator voice to use. This is a list of the narrator voices on your computer.

### Volume
Set the volume of the narrator.

### Speaking Rate
Set the pace of how fast the narrator should speak.

### Maximum Characters
Set the maximum number of characters in a TTS message. This only applies to text-to-speech triggered by the command or chat message. This does not apply to alert messages.

Use 0 for no limit on characters.

### Maximum Characters Message
Message to send to viewers when a TTS message is too long.

## TTS Command
In this section, you can customize a command that uses text-to-speech.

### Command Name
Set the command to use for text-to-speech.

### Permission level
Set the viewer rank/role required to use the TTS command.

### Permission level info
Set the user, rank, or tier for permission. Only used with certain permission levels: User_Specific, Min_Rank, Min_Points, Min_Hours.

### Cost (Points)
The number of points required to use the TTS command.

### TTS Message Format
Customize the message read by the narrator. The following variables will get replaced.
- *{user}* will be replaced with the viewer's username
- *{message}* will be replaced with the chat message

## TTS Command Usage
In this section, you can customize the usage for the TTS Command that uses text-to-speech.

### Usage
Determine how viewer's can use the TTS command. Options allow support for messages through discord and whispers.

### Send Usage Reply
Enable this to send a message to a viewer when they attempt to trigger the command from an invalid location. For example, this applies when the **Usage** is *Stream Chat* and a viewer attempts to trigger the command via Discord.

### Usage Reply Message
This is the message to send to a viewer who triggers the command from an invalid location.

## TTS Command Cooldown
In this section, you can customize a cooldown for the TTS Command that uses text-to-speech.

### Use Cooldown Message
Enable this to send a message when the command is on cooldown.

### Caster ignores cooldown
Enables the Caster to ignore the cooldown.

### Cooldown in seconds
Set the number of seconds before the TTS command can be used again.

### Cooldown Response
The message that the bot will display when the command is on cooldown.
- *{user}* will be replaced with the viewer's username
- *{cooldown}* will be replaced with the time remaining

### User cooldown in seconds
Set the number of seconds before a user can use the TTS command again.

### User Cooldown Response
The message that the bot will display when the command is on user cooldown
- *{user}* will be replaced with the viewer's username
- *{cooldown}* will be replaced with the time remaining

## TTS Chat Messages
In this section, you can toggle text-to-speech for ALL chat messages

### TTS All Chat Messages
Enable Text-To-Speech for all messages

### Exclude Reading Commands
Exclude reading messages that start with an exclamation point (!).

### TTS Message Format
Customize the message read by the narrator. The following variables will get replaced.
- *{user}* will be replaced with the viewer's username
- *{message}* will be replaced with the chat message

## TTS Chat Messages Usage
In this section, you can customize the usage for triggering text-to-speech via a message.

### Usage
Determine how viewer's can trigger text-to-speech. Options allow support for messages through discord and whispers.

### Send Usage Reply
Enable this to send a message to a viewer when they attempt to trigger the command from an invalid location. For example, this applies when the **Usage** is *Stream Chat* and a viewer attempts to trigger the command via Discord.

### Usage Reply Message
This is the message to send to a viewer who triggers the command from an invalid location.

## TTS Overlay
Text-to-speech messages can be displayed on a customizable overlay.

### Exclude Alerts from Overlay
Enable this to not display alert text-to-speech messages on the overlay.

### Overlay Message Format
Use this to format the message displayed on the overlay when triggered via command, chat messages, or messages included with alerts.

**Note:** This format will not apply to alert responses but WILL apply for messages included with alerts.

### Font Color, Font Outline, Font Shadow, Font Size, Font Family
Customize how the font looks on the overlay. Font family must be an available font on your computer.

### Background Color
Set the background color of the overlay.

### Border Color
Set the border color of the overlay.

### Horizontal/Vertical Align
Control the positioning of the overlay within the browser source by aligning the overlay to the left, center, or right and top, center, or bottom.

### Animate In/Out
Choose which animate.css animations to use when displaying the overlay.

## Alert Types
There are alert types across Mixer, Streamlabs, Twitch, and Youtube that are customizable. To save space, below is a summary of setting types.

### Enabled
Enable TTS for the given alert.

### Delay (seconds)
Delay in seconds to read the alert after receiving it. If two alerts are received simultaneously, the second's delay may be lost.

This setting is an attempt to delay TTS until after alert sfx is finished. Unfortunately, the script receives alerts *instantly* as opposed to through the queue that Streamlabs provides.

### Alert Message
The format of the alert to be read by text-to-speech. There are a number of variables available per alert type. Hover over the message in the settings for a detailed list for that alert.
- *{name}* will be replaced with the username
- *{amount}* will be replaced with a number for that alert (viewers, raiders, bits, etc.)
- *{isPlural}* is sometimes used to provide an 's' when amount > 1
- *{tier}* is the Twitch subscription tier
- *{months}* is the number of months of a subscription
- *{gifter}* is the gifter of a Twitch sub
- *{recipients}* is the comma-delimited list of viewers that are gifted subs when more than 1 sub is gifted to the channel

## Banned Words

### Banned Words Setting
Choose whether to skip messages with banned words or replace the words.

### Match Whole Words Only
Enable this to match words in the banned.txt file exactly. If disabled (unchecked), partial words will be matched. As an example, if **fu** is a banned word and the message contains **fudge**, the message will get blocked if this setting is unchecked. This helps avoid trolls that combine words together.

### Banned Word Replacement
This field is used to replace banned words when found in messages if *Replace Banned Words* was selected as the **Banned Words Setting**.

### Open banned.txt
Edit this file to control what words or phrases are banned from TTS. Each banned word or phrase should be on its own line.

## Streamlabs Token

### Streamlabs Socket Token
**Your Socket API Token** from https://streamlabs.com/dashboard#/settings/api-settings. See the *Usage* section for details.

***

# Copyright

This script was made by **Kruiser8** (https://twitch.tv/kruiser8) and is licensed under the *Creative Commmons Attribution 4.0 International License (CC BY 4.0)*

For License information, visit https://creativecommons.org/licenses/by/4.0/
