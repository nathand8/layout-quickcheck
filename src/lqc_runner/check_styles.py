""" One-off Script
Used for generating styles with a config file.
The styles generated are printed out.

This is a good script to run to check if the config outputs
styles in the frequency expected.
"""


import argparse

from lqc.config.config import Config, parse_config
from lqc.generate.css import style_data
from lqc.generate.css.style_generator import StyleGenerator

DEFAULT_CONFIG_FILE = "./config/preset-default.config.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Generate examples of style values")
    parser.add_argument("-n", "--number-values", help="the number of values to generate for each style", type=int, default=10)
    parser.add_argument("-s", "--styles", nargs="+", help="list of styles to generate values for", required=True)
    parser.add_argument("-c", "--config-file", help="path to config file to use", type=str, default=DEFAULT_CONFIG_FILE)
    args = parser.parse_args()

    # Initialize Config
    config = parse_config(args.config_file)
    Config(config)

    def generate_style(style_name):
        style_value_generator = StyleGenerator()
        for current_style in style_data["data"]:
            if current_style["name"] == style_name:
                gen = style_value_generator.pickGenerator(current_style)
                if gen:
                    return gen()
                else:
                    return None

    for style_name in args.styles:
        print(f"\n{style_name}")
        for _ in range(args.number_values):
            style_value = generate_style(style_name)
            print(f"{style_name}: {style_value};")