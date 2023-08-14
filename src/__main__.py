try:
    from .discord_webhook_ruiner import main
except ImportError:
    from discord_webhook_ruiner import main


if __name__ == '__main__':
    main()
