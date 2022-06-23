import yaml
import json

with open('Swagger_specification.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

with open('output/Swagger_configuration.txt', 'w') as f:
    output = json.dumps(configuration, separators=(',', ":"))
    replaced = output.replace('"', '\\"')
    f.write("const char * swaggerJSON = " + '"' + str(replaced) + '";')

print("Done!")
