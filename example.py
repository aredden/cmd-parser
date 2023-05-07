import random
from cmd_parser import CommandParser

cmd = "a wizard wearing balenciaga fashion, highly detailed, bokeh, sigma 40mm -c 9 -2c 11 -neg blurry, low-resolution, messy, boring, jpeg-artifacts -3c 12.5"

# Create command parser. 
# remaining_text_dest is the destination key in the parsed dictionary which will hold the text that remains after parsing command flag arguments.
cmd_parser = CommandParser(remaining_text_dest="prompt")

# Command types that must be given to each new subcommand to determine which regex to use - (INT, FLOAT, STR, BOOL):
cmdtype = cmd_parser.cmdtypes

# Add command flags to command parser.
cmd_parser = (
    cmd_parser.add_command("c", cmdtype.INT, "guidance_scale")
    .add_command("s", cmdtype.INT, "seed", default=lambda: random.randint(0, 999999))
    .add_command("neg", cmdtype.STR, "negative_prompt")
    .add_command("2c", cmdtype.FLOAT, "second_guidance_scale")
    .add_command("3c", cmdtype.FLOAT, "third_guidance_scale")
    .add_command("figs", cmdtype.BOOL, "figures_only")
)

# Parse command arguments from a string into a dictionary.
arguments = cmd_parser.parse(cmd)


print(arguments)
# prints:
{
    "guidance_scale": 9,
    "seed": 375977,
    "negative_prompt": "blurry, low-resolution, messy, boring, jpeg-artifacts",
    "second_guidance_scale": 11.0,
    "third_guidance_scale": 12.5,
    "figures_only": False,
    "prompt": "a wizard wearing balenciaga fashion, highly detailed, bokeh, sigma 40mm",
}
