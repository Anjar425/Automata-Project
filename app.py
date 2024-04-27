from flask import Flask, render_template, request, redirect, url_for
from regex2nfafinal import convertToNFA
import logging
import graphviz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    regex = request.form.get('regex')  # Ambil nilai 'regex' dari formulir

    logging.debug(f"Regular expression: {regex}")
    nfa = convertToNFA(regex)
    logging.debug(f"NFA: {nfa}")

    # Visualisasi NFA
    dot = graphviz.Digraph(comment='NFA Visualization')
    dot.graph_attr['rankdir'] = 'LR'

    # Buat node dan edge sesuai dengan NFA
    for state in nfa['states']:
        dot.node(state)
    for arc in nfa['transition_matrix']:
        start, label, end = arc
        dot.edge(start, end, label)

    # Simpan gambar ke file
    dot.render('static/nfa_graph', format='svg', cleanup=False)

    nfa_generated = True
    return render_template('index.html', nfa_image='static/nfa_graph.svg', nfa_generated=nfa_generated )


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)  # Aktifkan logging debug
    app.run(debug=True)
