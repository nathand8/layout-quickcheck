import argparse
from css_generators.style_data import style_data
from css_generators.style_generator import StyleGenerator
from css_generators.style_generator_config import StyleGeneratorConfig
from compare import parse_config
from css_generators.util.color import generate

DEFAULT_CONFIG_FILE = "./config/default.config.json"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Generate examples of style values")
    parser.add_argument("-n", "--number-values", help="the number of values to generate for each style", type=int, default=10)
    parser.add_argument("-s", "--styles", nargs="+", help="list of styles to generate values for", required=True)
    parser.add_argument("-c", "--config-file", help="path to config file to use", type=str, default=DEFAULT_CONFIG_FILE)
    args = parser.parse_args()

    # Initialize Config
    config = parse_config(args.config_file)
    StyleGeneratorConfig(config)

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