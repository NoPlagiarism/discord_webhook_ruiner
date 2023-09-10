# Discord Scam Webhook Destroyer (Ruiner) [BETA]
> Now, let's destroy those "Free Robux" guys

## Install
### pipx (recommended)
```commandline
pipx install git+https://github.com/NoPlagiarism/discord_webhook_ruiner
```

### git clone (with poetry)
```commandline
git clone https://github.com/NoPlagiarism/discord_webhook_ruiner
cd discord_webhook_ruiner
poetry install
poetry shell
python src
```

### git clone (with requirements.txt)
> better use poetry, requirements exported using "poetry export"

```commandline
git clone https://github.com/NoPlagiarism/discord_webhook_ruiner
cd discord_webhook_ruiner

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src
```

## Features
- Delete webhook
- Get info about webhook, including creator (only pretty JSON available for now)

## To-Do
- [ ] Display webhook info prettier
- [ ] Send messages
  - [ ] Support templates (don't forget to change username & avatar to get them crazy)
    - [ ] Support input in there?
  - [ ] Send multiple time
    - [ ] Send until destroy?

Thanks to [Discohook](https://discohook.org/), great tool

## Alternatives
- [WebShook](https://github.com/Francesco2426/WebShook)
