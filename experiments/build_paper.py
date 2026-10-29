"""Convert the complete Markdown manuscript to an editable LaTeX body."""
from pathlib import Path
import os,re,shutil,subprocess

root=Path(__file__).resolve().parents[1]
paper=root/'paper'
text=(paper/'manuscript.md').read_text(encoding='utf-8')
assert re.findall(r'^## (\d+)\.',text,re.M)==list(map(str,range(1,7)))
assert text.count('## Abstract\n')==1 and text.count('## References\n')==1
assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',text)
latex=paper/'latex'
assert (latex/'main.tex').exists(), 'Create the dedicated LaTeX project first.'
pandoc=os.environ.get('PANDOC') or shutil.which('pandoc')
if not pandoc:raise RuntimeError('Install Pandoc or set PANDOC executable.')
subprocess.run([pandoc,str(paper/'manuscript.md'),'-f',
    'markdown+tex_math_dollars+raw_tex+autolink_bare_uris-implicit_figures',
    '-t','latex','--no-highlight','-o',str(latex/'body.tex')],check=True)
body=(latex/'body.tex').read_text(encoding='utf-8').replace('../figures/','images/')
title=text.splitlines()[0].removeprefix('# ')
body=body.replace(r'\section{',r'\section['+title+r']{\raggedright ',1)
body=re.sub(r'\\texttt\{([^{}\n ]+)\}',lambda m:r'\nolinkurl{'+m[1].replace(r'\_','_')+'}',body)
def small_table(match):
    value=match[0].replace(r'\begin{longtable}[]',r'\begin{tabular}')
    value=value.replace('\\endhead\n\\bottomrule\\noalign{}\n\\endlastfoot\n','')
    value=value.replace(r'\end{longtable}',r'\bottomrule\noalign{}'+'\n'+r'\end{tabular}')
    return '\n'+r'\begin{minipage}{\linewidth}\small'+'\n'+value+'\n'+r'\end{minipage}'+'\n'
body,n=re.subn(r'\\begin\{longtable\}.*?\\end\{longtable\}',small_table,body,flags=re.S)
assert n==1,n
def keep_figure(match):
    return r'\begin{minipage}{\linewidth}'+'\n'+match[0]+'\n'+r'\end{minipage}'
body,figs=re.subn(r'\\pandocbounded\{\\includegraphics\[[^\n]+\}\}\n\nFigure [123]\. .*?(?=\n\n)',
    keep_figure,body,flags=re.S)
assert figs==3,figs
heading=r'\subsection{References}\label{references}'
assert body.count(heading)==1
body=body.replace(heading,r'\clearpage'+'\n'+r'\begingroup\small\raggedright'+'\n'+heading)+'\n'+r'\endgroup'+'\n'
(latex/'body.tex').write_text(body,encoding='utf-8',newline='\n')
(latex/'images').mkdir(exist_ok=True)
for image in (root/'figures').glob('*.png'):
    shutil.copy2(image,latex/'images'/image.name)
print({'body_words_regex':len(re.findall(r'\b[\w-]+\b',text.split('## References')[0])),
       'tables':n,'figures':len(list((root/'figures').glob('*.png')))})
