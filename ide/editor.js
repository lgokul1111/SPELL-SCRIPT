let editorView = null;

// SpellScript syntax
CodeMirror.defineMode("spellscript", function() {
  return {
    token: function(stream, state) {
      if (stream.eatSpace()) return null;

      if (stream.match(/^"[^"]*"/)) return "string";
      if (stream.match(/^\d+/)) return "number";
      if (stream.match(/^(spell|potion|when|otherwise|repeat)\b/)) return "keyword";
      if (stream.match(/^[=+\-*\/<>]/)) return "operator";

      stream.next();
      return null;
    }
  };
});

// Create editor
function createEditor() {
  editorView = CodeMirror(document.getElementById("editor"), {
    value: 'spell "Hello Wizard"',
    mode: "spellscript",
    lineNumbers: true,
    lineWrapping: false,
    theme: "default"
  });
}

window.createEditor = createEditor;
window.getEditorCode = function() {
  return editorView.getValue();
};