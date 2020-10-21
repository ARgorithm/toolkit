if __name__ == "__main__":
    
    from wasabi import msg
    import sys

    from ARgorithmToolkit.cli import init,submit,help,test,delete
    
    commands = {
        "init" : init,
        "submit" : submit,
        "test": test,
        "delete" : delete,
        "help" : help
    }

    if len(sys.argv) == 1:
        msg.info("Available commands", ", ".join(commands), exits=1)
    command = sys.argv.pop(1)
    sys.argv[0] = "spacy %s" % command
    if command in commands:
        commands[command](*sys.argv[1:])
    else:
        available = "Available: {}".format(", ".join(commands))
        msg.fail("Unknown command: {}".format(command), available, exits=1)