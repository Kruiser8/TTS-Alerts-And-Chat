#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Text-To-Speech for Alerts and Chat Messages

	1.0.0
		Initial public release

"""

#---------------------------------------
# Script Import Libraries
#---------------------------------------
import os
import codecs
import json
from collections import OrderedDict
import time
import re
import threading
import clr
clr.AddReference("IronPython.Modules.dll")
clr.AddReference('System.Speech')
clr.AddReferenceToFileAndPath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "StreamlabsEventReceiver.dll"))
from System.Speech.Synthesis import SpeechSynthesizer
from StreamlabsEventReceiver import StreamlabsEventClient

#---------------------------------------
# Script Information
#---------------------------------------
ScriptName = "TTS Alerts and Chat"
Website = "https://www.twitch.tv/kruiser8"
Description = "Text-to-speech for streamlabs alerts and chat messages."
Creator = "Kruiser8"
Version = "1.0.0"

#---------------------------------------
# Script Variables
#---------------------------------------

# Socket Receiver
EventReceiver = None

# Settings file location
SettingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

# UI Config file location
UIConfigFile = os.path.join(os.path.dirname(__file__), "UI_Config.json")

# Banned words file
BannedFile = os.path.join(os.path.dirname(__file__), "banned.txt")

SubPlanMap = {
	"Prime": "Prime",
	"1000": "Tier 1",
	"2000": "Tier 2",
	"3000": "Tier 3"
}

#---------------------------------------
# Script Classes
#---------------------------------------
class Settings(object):
	""" Load in saved settings file if available else set default values. """
	def __init__(self, settingsfile=None):
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8")
		except:
			self.VoiceName = ""
			self.Volume = 80
			self.Rate = 0
			self.TTSCommand = "!tts"
			self.TTSCommandPermission = "Caster"
			self.TTSCommandPermissionInfo = ""
			self.TTSCommandCost = 500
			self.TTSCommandMessage = "{user} says, {message}"
			self.TTSUseCD = False
			self.TTSCasterCD = True
			self.TTSCooldown = 0
			self.TTSOnCooldown = "{user} the command is still on cooldown for {cooldown} seconds!"
			self.TTSUserCooldown = 10
			self.TTSOnUserCooldown = "{user} the command is still on user cooldown for {cooldown} seconds!"
			self.TTSAllChat = False
			self.TTSAllChatExcludeCommands = True
			self.TTSAllChatMessage = "{user} says, {message}"
			self.MixerOnFollow = False
			self.MixerFollowDelay = 0
			self.MixerFollowMessage = "{name} has followed."
			self.MixerOnHost = False
			self.MixerHostMinimum = 0
			self.MixerHostDelay = 0
			self.MixerHostMessage = "{name} has hosted you with {amount} viewer{isPlural}."
			self.MixerOnSub = False
			self.MixerIncludeSubMessage = True
			self.MixerSubDelay = 0
			self.MixerSubMessage = "{name} has subscribed ({tier})."
			self.MixerResubMessage = "{name} has resubscribed ({tier}) for {months} months."
			self.StreamlabsOnDonation = False
			self.StreamlabsIncludeDonationMessage = True
			self.StreamlabsDonationMinimum = 1
			self.StreamlabsDonationDelay = 0
			self.StreamlabsDonationMessage = "{name} donated {amount}."
			self.TwitchOnCheer = False
			self.TwitchIncludeCheerMessage = True
			self.TwitchCheerMinimum = 100
			self.TwitchCheerDelay = 0
			self.TwitchCheerMessage = "{name} has used {amount} bit{isPlural}."
			self.TwitchOnFollow = False
			self.TwitchFollowDelay = 0
			self.TwitchFollowMessage = "{name} has followed."
			self.TwitchOnHost = False
			self.TwitchHostMinimum = 0
			self.TwitchHostDelay = 0
			self.TwitchHostMessage = "{name} has hosted you with {amount} viewer{isPlural}."
			self.TwitchOnRaid = False
			self.TwitchRaidMinimum = 0
			self.TwitchRaidDelay = 0
			self.TwitchRaidMessage = "{name} has raided you with a party of {amount}."
			self.TwitchOnSub = False
			self.TwitchIncludeSubMessage = True
			self.TwitchSubDelay = 0
			self.TwitchSubMessage = "{name} has subscribed ({tier})."
			self.TwitchResubMessage = "{name} has resubscribed ({tier}) for {months} months."
			self.TwitchGiftMessage = "{gifter} has gifted a sub ({tier}) to {name} ({months} month{isPlural})."
			self.TwitchGiftMassMessage = "{gifter} has gifted {amount} subs to the channel: {recipients}."
			self.YoutubeOnFollow = False
			self.YoutubeFollowDelay = 0
			self.YoutubeFollowMessage = "{name} has followed."
			self.YoutubeOnSub = False
			self.YoutubeIncludeSubMessage = True
			self.YoutubeSubDelay = 0
			self.YoutubeSubMessage = "{name} has subscribed ({tier})."
			self.YoutubeResubMessage = "{name} has resubscribed ({tier}) for {months} months."
			self.YoutubeOnSuperchat = False
			self.YoutubeIncludeSuperchatMessage = True
			self.YoutubeSuperchatMinimum = 5
			self.YoutubeSuperchatDelay = 0
			self.YoutubeSuperchatMessage = "{name} donated {amount}."
			self.BannedAction = "Skip Messages with a Banned Word"
			self.BannedReplacement = ""
			self.SocketToken = None

	def Reload(self, jsondata):
		""" Reload settings from Streamlabs user interface by given json data. """
		self.__dict__ = json.loads(jsondata, encoding="utf-8")

	def Save(self, settingsfile):
		""" Save settings contained within to .json and .js settings files. """
		try:
			with codecs.open(settingsfile, encoding="utf-8-sig", mode="w+") as f:
				json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
			with codecs.open(settingsfile.replace("json", "js"), encoding="utf-8-sig", mode="w+") as f:
				f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8', ensure_ascii=False)))
		except:
			Parent.Log(ScriptName, "Failed to save settings to file.")

class UIConfig(object):
	""" Load in saved settings file if available else set default values. """
	def __init__(self, uiconfigfile=None):
		try:
			with codecs.open(uiconfigfile, encoding="utf-8-sig", mode="r") as f:
				self.__dict__ = json.load(f, encoding="utf-8", object_pairs_hook=OrderedDict)
		except:
			Parent.SendStreamWhisper(Parent.GetChannelName(), "Failed to read UIConfig file: " + str(sys.exc_info()[1]))

	def Save(self, uiconfigfile):
		""" Save UI Config contained within to .json file. """
		if len(self.__dict__) > 0:
			try:
				with codecs.open(uiconfigfile, encoding="utf-8-sig", mode="w+") as f:
					json.dump(self.__dict__, f, encoding="utf-8", ensure_ascii=False)
			except:
				Parent.SendStreamWhisper(Parent.GetChannelName(), "Failed to save ui config to file.")

#---------------------------------------
# Event Receiver Functions
#---------------------------------------
def EventReceiverConnected(sender, args):
	Parent.Log(ScriptName, "Connected")
	return

def EventReceiverDisconnected(sender, args):
	Parent.Log(ScriptName, "Disconnected")

def EventReceiverEvent(sender, args):
	handleEvent(sender,args)

def handleEvent(sender, args):
	# Just grab the all data in from the event
	evntdata = args.Data

	# Check if it contains data and for what streaming service it is
	if evntdata and evntdata.For == "twitch_account":

		if evntdata.Type == "follow" and ScriptSettings.TwitchOnFollow:
			for message in evntdata.Message:
				ttsMessage = ScriptSettings.TwitchFollowMessage.format(name=message.Name)
				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.TwitchFollowDelay)

		elif evntdata.Type == "bits" and ScriptSettings.TwitchOnCheer:
			s = ''
			for message in evntdata.Message:
				if message.Amount >= ScriptSettings.TwitchCheerMinimum:
					if message.Amount > 1:
						s = 's'
					else:
						s = ''
					ttsMessage = ScriptSettings.TwitchCheerMessage.format(name=message.Name, amount=message.Amount, isPlural=s)
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.TwitchCheerDelay, ScriptSettings.TwitchIncludeCheerMessage, message.Message)

		elif evntdata.Type == "host" and ScriptSettings.TwitchOnHost:
			s = ''
			for message in evntdata.Message:
				if int(message.Viewers) >= ScriptSettings.TwitchHostMinimum:
					if message.Viewers > 1:
						s = 's'
					else:
						s = ''
					ttsMessage = ScriptSettings.TwitchHostMessage.format(name=message.Name, amount=str(message.Viewers), isPlural=s)
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.TwitchHostDelay)

		elif evntdata.Type == "raid" and ScriptSettings.TwitchOnRaid:
			for message in evntdata.Message:
				if int(message.Raiders) >= ScriptSettings.TwitchRaidMinimum:
					ttsMessage = ScriptSettings.TwitchRaidMessage.format(name=message.Name, amount=str(message.Raiders))
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.TwitchRaidDelay)

		elif evntdata.Type == "subscription" and ScriptSettings.TwitchOnSub:
			s = ''
			if len(evntData.Message) > 1 and evntData.Message[0].Gifter:
				names = []
				for message in evntdata.Message:
					names.append(message.Name)
				giftees = ', '.join(names)
				ttsMessage = ScriptSettings.TwitchGiftMassMessage.format(recipients=giftees, gifter=message.Gifter, amount=len(names))
			else:
				for message in evntdata.Message:
					tier = SubPlanMap[str(message.SubPlan)]
					ttsMessage = ''
					if message.Gifter:
						if message.Months > 1:
							s = 's'
						else:
							s = ''
						ttsMessage = ScriptSettings.TwitchGiftMessage.format(name=message.Name, gifter=message.Gifter, tier=tier, months=message.Months, isPlural=s)
					else:
						if message.Months == 1:
							ttsMessage = ScriptSettings.TwitchSubMessage.format(name=message.Name, tier=tier, months=message.Months)
						else:
							ttsMessage = ScriptSettings.TwitchResubMessage.format(name=message.Name, tier=tier, months=message.Months)

				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.TwitchSubDelay, ScriptSettings.TwitchIncludeSubMessage, message.Message)

	elif evntdata and evntdata.For == "mixer_account":

		if evntdata.Type == "follow" and ScriptSettings.MixerOnFollow:
			for message in evntdata.Message:
				ttsMessage = ScriptSettings.MixerFollowMessage.format(name=message.Name)
				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.MixerFollowDelay)

		elif evntdata.Type == "subscription" and ScriptSettings.MixerOnSub:
			for message in evntdata.Message:
				ttsMessage = ''
				if message.Months == 1:
					ttsMessage = ScriptSettings.MixerSubMessage.format(name=message.Name, tier=tier, months=message.Months)
				else:
					ttsMessage = ScriptSettings.MixerResubMessage.format(name=message.Name, tier=tier, months=message.Months)

				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.MixerSubDelay, ScriptSettings.MixerIncludeSubMessage, message.Message)

		elif evntdata.Type == "host" and ScriptSettings.MixerOnHost:
			s = ''
			for message in evntdata.Message:
				if int(message.Viewers) >= ScriptSettings.MixerHostMinimum:
					if message.Viewers > 1:
						s = 's'
					else:
						s = ''
					ttsMessage = ScriptSettings.MixerHostMessage.format(name=message.Name, amount=str(message.Viewers), isPlural=s)
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.MixerHostDelay)

	elif evntdata and evntdata.For == "streamlabs":
		if evntdata.Type == "donation" and ScriptSettings.StreamlabsOnDonation:
			for message in evntdata.Message:
				if float(message.Amount) >= ScriptSettings.StreamlabsDonationMinimum:
					ttsMessage = ScriptSettings.StreamlabsDonationMessage.format(name=message.Name, amount=str(message.FormattedAmount))
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.StreamlabsDonationDelay, ScriptSettings.StreamlabsIncludeDonationMessage, message.Message)

	elif evntdata and evntdata.For == "youtube_account":
		if evntdata.Type == "follow" and ScriptSettings.YoutubeOnFollow:
			for message in evntdata.Message:
				ttsMessage = ScriptSettings.YoutubeFollowMessage.format(name=message.Name)
				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.YoutubeFollowDelay)

		elif evntdata.Type == "subscription" and ScriptSettings.YoutubeOnSub:
			for message in evntdata.Message:
				ttsMessage = ''
				if message.Months == 1:
					ttsMessage = ScriptSettings.YoutubeSubMessage.format(name=message.Name, tier=tier, months=message.Months)
				else:
					ttsMessage = ScriptSettings.YoutubeResubMessage.format(name=message.Name, tier=tier, months=message.Months)

				SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.YoutubeSubDelay)

		elif evntdata.Type == "superchat" and ScriptSettings.YoutubeOnSuperchat:
			for message in evntdata.Message:
				if float(message.Amount) >= ScriptSettings.YoutubeSuperchatMinimum:
					ttsMessage = ScriptSettings.YoutubeSuperchatMessage.format(name=message.Name, amount=str(message.FormattedAmount))
					SendTTSMessagesWithDelay(ttsMessage, ScriptSettings.YoutubeSuperchatDelay, ScriptSettings.YoutubeIncludeSuperchatMessage, message.Message)

#---------------------------------------
# Script Functions
#---------------------------------------
def updateUIConfig():
	voices = []
	for voice in spk.GetInstalledVoices():
		info = voice.VoiceInfo
		voices.append(info.Name)

	UIConfigs = UIConfig(UIConfigFile)
	UIConfigs.VoiceName['items'] = voices

	if ScriptSettings.VoiceName not in voices:
		ScriptSettings.VoiceName = ''
		ScriptSettings.Save(SettingsFile)

	UIConfigs.Save(UIConfigFile)

def SendTTSMessage(voice, message):
	if ScriptSettings.BannedAction == 'Skip Messages with a Banned Word':
		if bool(reBanned.search(message)):
			return
	else:
		message = reBanned.sub(ScriptSettings.BannedReplacement, message)
	try:
		voice.Speak(message)
	except Exception as e:
		Parent.SendStreamWhisper(Parent.GetChannelName(), 'TTS Failed, please see logs')
		Parent.Log(ScriptName, str(e.args))

def SendTTSMessagesWithDelay(message, delay, includeExtra = False, extraMessage = ''):
	if delay > 0:
		time.sleep(delay)

	global spk
	SendTTSMessage(spk, message)
	if includeExtra:
		SendTTSMessage(spk, extraMessage)

#---------------------------------------
# Chatbot Initialize Function
#---------------------------------------
def Init():
	# Load settings from file and verify
	global ScriptSettings
	ScriptSettings = Settings(SettingsFile)

	global spk
	spk = SpeechSynthesizer()
	spk.Rate = ScriptSettings.Rate
	spk.Volume = ScriptSettings.Volume

	updateUIConfig()

	banned = []
	with open(BannedFile) as f:
		banned = f.readlines()

	banned = [x.strip() for x in banned]
	banned = sorted(set(banned))

	with open(BannedFile, 'w') as f:
		for word in banned:
			print >>f, word

	global reBanned
	reBanned = re.compile(r"({0})".format('|'.join(banned)))

	if ScriptSettings.VoiceName != '':
		spk.SelectVoice(ScriptSettings.VoiceName)

	# Init the Streamlabs Event Receiver
	global EventReceiver
	EventReceiver = StreamlabsEventClient()
	EventReceiver.StreamlabsSocketConnected += EventReceiverConnected
	EventReceiver.StreamlabsSocketDisconnected += EventReceiverDisconnected
	EventReceiver.StreamlabsSocketEvent += EventReceiverEvent

	# Auto Connect if key is given in settings
	if ScriptSettings.SocketToken:
		EventReceiver.Connect(ScriptSettings.SocketToken)

	# End of Init
	return

#---------------------------------------
# Chatbot Save Settings Function
#---------------------------------------
def ReloadSettings(jsondata):
	# Reload newly saved settings and verify
	ScriptSettings.Reload(jsondata)

	if ScriptSettings.VoiceName != '':
		global spk
		spk.SelectVoice(ScriptSettings.VoiceName)

	spk.Rate = ScriptSettings.Rate
	spk.Volume = ScriptSettings.Volume

	global EventReceiver
	if not EventReceiver.IsConnected and ScriptSettings.SocketToken:
		EventReceiver.Connect(ScriptSettings.SocketToken)
	elif EventReceiver.IsConnected and not ScriptSettings.SocketToken:
		EventReceiver.Disconnect()

	# End of ReloadSettings
	return

#---------------------------------------
#	Chatbot Script Unload Function
#---------------------------------------
def Unload():
	global EventReceiver
	if EventReceiver.IsConnected:
		EventReceiver.Disconnect()

#---------------------------------------
# Chatbot Execute Function
#---------------------------------------
def Execute(data):
	if data.IsChatMessage():
		if ScriptSettings.TTSAllChat:
			if not ScriptSettings.TTSAllChatExcludeCommands or data.Message[0] != '!':
				message = ScriptSettings.TTSAllChatMessage.format(user=data.UserName, message=data.Message)
				messageThread = threading.Thread(target=SendTTSMessage, args=(spk, message))
				messageThread.daemon = True
				messageThread.start()
		else:
			command = data.GetParam(0)

			if command == ScriptSettings.TTSCommand:
				if HasPermission(data, ScriptSettings.TTSCommandPermission, ScriptSettings.TTSCommandPermissionInfo):
					if not IsOnCooldown(data, ScriptSettings.TTSCommand, ScriptSettings.TTSCasterCD, ScriptSettings.TTSUseCD, ScriptSettings.TTSOnCooldown, ScriptSettings.TTSOnUserCooldown):
						if HasCurrency(data, ScriptSettings.TTSCommandCost):
							commandOffset = len(ScriptSettings.TTSCommand) + 1
							message = ScriptSettings.TTSCommandMessage.format(user=data.UserName, message=data.Message[commandOffset:])
							messageThread = threading.Thread(target=SendTTSMessage, args=(spk, message))
							messageThread.daemon = True
							messageThread.start()

							Parent.AddUserCooldown(ScriptName, ScriptSettings.TTSCommand, data.User, ScriptSettings.TTSUserCooldown)
	    					Parent.AddCooldown(ScriptName, ScriptSettings.TTSCommand, ScriptSettings.TTSCooldown)

	# End of execute
	return

#---------------------------------------
# Chatbot Execute Helper Functions
#---------------------------------------
def HasPermission(data, permission, permissionInfo):
    """Returns true if user has permission and false if user doesn't"""
    if not Parent.HasPermission(data.User, permission, permissionInfo):
        return False
    return True

def IsOnCooldown(data, command, casterCD, useCD, cooldownMessage, userCooldownMessage):
    """Return true if command is on cooldown and send cooldown message if enabled"""
    #introduce globals for cooldown management
    cooldown = Parent.IsOnCooldown(ScriptName, command)
    userCooldown = Parent.IsOnUserCooldown(ScriptName, command, data.User)
    caster = (Parent.HasPermission(data.User, "Caster", "") and casterCD)

    #check if command is on cooldown
    if (cooldown or userCooldown) and caster is False:

        #check if cooldown message is enabled
        if useCD:

            #set variables for cooldown
            cooldownDuration = Parent.GetCooldownDuration(ScriptName, command)
            userCDD = Parent.GetUserCooldownDuration(ScriptName, command, data.User)

            #check for the longest CD!
            if cooldownDuration > userCDD:

                #set cd remaining
                m_CooldownRemaining = cooldownDuration

                #send cooldown message
                message = cooldownMessage.format(user=data.UserName, cooldown=m_CooldownRemaining)
                Parent.SendStreamMessage(message)

            else: #set cd remaining
                m_CooldownRemaining = userCDD

                #send usercooldown message
                message = userCooldownMessage.format(user=data.UserName, cooldown=m_CooldownRemaining)
                Parent.SendStreamMessage(message)
        return True
    return False

def HasCurrency(data, cost):
    if (cost == 0) or (Parent.RemovePoints(data.User, data.UserName, cost)):
        return True
    return False

#---------------------------------------
# Chatbot Tick Function
#---------------------------------------
def Tick():

	# End of Tick
	return

#---------------------------------------
# Chatbot Parameter Parser
#---------------------------------------
def Parse(parseString, user, target, message):

	# Return unaltered parseString
	return parseString

#---------------------------------------
# Chatbot Button Function
#---------------------------------------
def OpenReadMe():
    """Open the README.txt in the scripts folder"""
    os.startfile(os.path.join(os.path.dirname(__file__), "README.txt"))

def OpenBannedFile():
	"""Open the banned.txt in the scripts folder"""
	os.startfile(os.path.join(os.path.dirname(__file__), "banned.txt"))

def OpenSocketToken():
    """Open Streamlabs API Settings"""
    OpenLink("https://streamlabs.com/dashboard#/settings/api-settings")

def OpenGithubRepository():
	"""Open the GitHub Repository for this script"""
	OpenLink("https://github.com/kruiser8/TTS-Alerts-And-Chat")

def OpenTwitter():
	"""Open the Twitter of the author"""
	OpenLink("https://twitter.com/kruiser8")

def OpenLink(link):
    """Open links through buttons in UI"""
    os.system("explorer " + link)
