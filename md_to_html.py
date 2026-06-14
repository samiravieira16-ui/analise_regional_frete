import markdown
import codecs
import sys

def convert_md_to_html(md_file, html_file):
    with codecs.open(md_file, mode="r", encoding="utf-8") as f:
        text = f.read()

    # Convert markdown to html
    html_content = markdown.markdown(text, extensions=['tables'])

    # CSS for a beautiful PDF print
    css = """
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1, h2, h3 { color: #2C3E50; }
        h1 { border-bottom: 2px solid #2C3E50; padding-bottom: 10px; }
        h2 { border-bottom: 1px solid #eee; padding-bottom: 5px; margin-top: 30px; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; border-radius: 4px; padding: 5px; margin: 15px 0; }
        table { border-collapse: collapse; width: 100%; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; }
        code { background-color: #f1f1f1; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }
        hr { border: 0; border-top: 1px solid #eee; margin: 30px 0; }
        @media print {
            body { padding: 0; }
            img { max-width: 100%; page-break-inside: avoid; }
            h2, h3 { page-break-after: avoid; }
            table { page-break-inside: avoid; }
        }
    </style>
    """

    final_html = f"<!DOCTYPE html><html><head><meta charset='utf-8'>{css}</head><body>{html_content}</body></html>"

    with codecs.open(html_file, "w", encoding="utf-8", errors="xmlcharrefreplace") as f:
        f.write(final_html)
    
    print(f"Gerado: {html_file}")

if __name__ == "__main__":
    convert_md_to_html("Relatorio_Analise_Frete.md", "outputs/Relatorio_Analise_Frete_Imprimir.html")
    convert_md_to_html("Relatorio_Dados_Numericos.md", "outputs/Relatorio_Dados_Numericos_Imprimir.html")
    convert_md_to_html("Relatorio_Limpeza_de_Dados.md", "outputs/Relatorio_Limpeza_de_Dados_Imprimir.html")
