from pathlib import Path

src=Path('.github/materializers/cptec_batch.py').read_text(encoding='utf-8')
src=src.replace("'methodology_url':'http://bancodedados.cptec.inpe.br/'", "'methodology_url':'https://www.cptec.inpe.br/faq/como-acessar-os-dados-da-pagina-de-banco-de-dados-do-cptec/'")
src=src.replace("'access_mechanism':", "'access_tool':")
src=src.replace("'machine_readable':", "'free_download':")
src=src.replace("'subset_support':", "'provider_attribution_required':")
src=src.replace("'subset_mechanism':", "'subset_support':")
src=src.replace("'distribution_notes':", "'notes':")
exec(compile(src, '.github/materializers/cptec_batch.py', 'exec'))
