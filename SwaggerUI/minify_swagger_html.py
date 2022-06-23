import minify_html

######################################################################################################################
# Opens SwaggerUI.html and minifies it, escapes all "-characters and outputs it to SwaggerUI_minified.txt ready to use
######################################################################################################################

with open('swagger_configs/SwaggerUI.html', 'r') as f:
    html_str = f.read()

minified = minify_html.minify(html_str,
                              do_not_minify_doctype=True,
                              minify_js=True,
                              keep_closing_tags=False,
                              keep_html_and_head_opening_tags=True,
                              keep_spaces_between_attributes=True,
                              remove_bangs=False,
                              remove_processing_instructions=False
                              )


replaced = minified.replace('"', '\\"')

with open('output/SwaggerUI_minified.txt', 'w') as f:
    f.write("const char * swaggerUI = " + '"' + str(replaced) + '";')

print("Done!")
