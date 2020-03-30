# slackservice
Slack Service for Family Law

<p align="center">
    <a href="https://github.com/tjdaley/slackservice/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/tjdaley/slackservice"></a>
    <a href="https://github.com/tjdaley/slackservice/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/tjdaley/slackservice"></a>
    <a href="https://github.com/tjdaley/slackservice/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/tjdaley/slackservice"><a>
    <img alt="Stage: Development" src="https://img.shields.io/badge/stage-Development-orange">
</p>
<p align="center">
    <a href="#purpose">Purpose</a> &bull;
    <a href="#installation">Installation</a> &bull;
    <a href="#implemented-utilities">Utilities</a> &bull;
    <a href="#virtual-environment">Virtual Env</a> &bull;
    <a href="#author">Author</a>
</p>

## Purpose
This Slack service, or "bot", is intended to provide attorneys with some quick utilities for handling
routine, but annoying tasks, such as calculating child support, computing step-down schedules, computing
withholding amounts, etc. It is a complement to the fuller functionality of Attorney Bot.

## Installation
```
git clone https://github.com/tjdaley/slackservice
cd slackservice
python3 -m venv ./app/bin/activate
python -m pip -r requirements.txt
```

## Implemented Utilities

### Calculate Child Support
This utility is implemented as a slash command:

```
/cs 
```

It does not process any parameters because I don't know how to set default values in a modal.

When it runs, a modal dialog will appear and prompt the user for basic information. (For a more rigorous
implementation that takes into consider multiple jobs and non-earned income AND produces trial exhibits,
see Attorney Bot.) All fields *above* the horizonatal line are required. Scrolling below the horizontal line
reveals additional, but less commonly used settings such as union dues and a self-employment flag.

After the user clicks the **CALCULATE** button, the modal is dismissed and a child support report appears
as an ephemeral message in the channel in which the slash command was invoked.

TODO: If you invoke the slash command from your DM or IM channel, you will NOT get a report. I don't know
why that is. It may be because the bot has to be installed by the user into their workspace?

## Virtual Environment

From the slackservice folder:

**To Activate** (*Linux ONLY*)
```
python3 -m venv ./app/bin/activate
```

**To Deactivate**
```
deactivate 
```

## Author

Thomas J. Daley, J.D. is an active family law litigation attorney practicing primarily in Collin County, Texas, an occassional mediator, and software developer.