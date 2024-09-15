from docutils import nodes
from sphinx.directives.code import CodeBlock

class InlineCodeBlock(CodeBlock):
    def run(self):
        # Parse out the language and inline directive like "nix class:expression"
        language, *directives = self.arguments[0].split()

        # Process any inline directive, e.g., setting classes
        options = self.options
        for directive in directives:
            if directive.startswith('class:'):
                options['classes'] = [directive[len('class:'):]]
        
        # Modify the first argument to only include the language (without directives)
        self.arguments[0] = language
        
        # Call the original CodeBlock directive
        return super().run()

def setup(app):
    app.add_directive('code-block', InlineCodeBlock)