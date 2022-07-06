import yaml
import json

minify = False

with open('swagger_configs/Swagger_specification.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

with open('output/Swagger_configuration.txt', 'w') as f:
    if minify:
        output = json.dumps(configuration, separators=(',', ":"))
        replaced = output.replace('"', '\\"')
        f.write("static const char * swaggerJSON = " + '"' + str(replaced) + '";')
    else:
        json.dump(configuration, f, indent=4)

print("Done!")
