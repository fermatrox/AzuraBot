# AzuraBot overview

AzuraBot is an plugin-based Open Source chatbot framework, written in
Python using the `asyncio` package. It can be used in two different ways:
- As a backend and middleware
- As a backend only

# Plugins

AzuraBot supports different types of plugins, which must also be
written in Python. 

## Interface plugins

Interface plugins are what gives AzuraBot the ability to communicate
with user. Each such plugin makes it possible for users to communicate
with AzuraBot using a specific protocol or service, for example IRC,
Slack, or Twitter.

## Intent selector plugins

Intent selector plugins have the role of selecting an intent for input
sent to AzuraBot by a user. That is, what is the "intent" of the
user - what do they want? Is their intent to get a weather report, or
to create a reminder?

## Intent plugins

Intent plugins provide the intents, or actions if you will, that the
user can request to have performed.

## Filter plugins

