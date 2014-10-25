# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2014-10-13 16:59
# modified : 2014-10-13 16:59
"""
Update bibliography using Markdown format.
"""

__author__="Johann-Mattis List"
__date__="2014-10-13"

from lingpyd.plugins.bibtex.bibtex import *

bib = BibTex('evobib/evobib.bib')


papers = [(k,bib[k]) for k in bib if ('List, J.-M.' in bib[k]['author_str'] or
'J.-M. List' in bib[k]['author_str']) and
        bib[k]['type'] not in 'customa,lecture,online']
talks = [(k,bib[k]) for k in bib if ('List, J.-M.' in bib[k]['author_str'] or 'J.-M. List' in bib[k]['author_str']) and bib[k]['type'] == 'customa']

lectures = [(k,bib[k]) for k in bib if ('List, J.-M.' in bib[k]['author_str'] or
        "J.-M. List" in bib[k]['author_str']) and bib[k]['type'] == 'lecture']


# write papers to file
with open('../papers.md', 'w') as f:
    f.write("---\n")
    f.write("title: Papers\n")
    f.write("type: research\n")
    f.write("layout: default\n")
    f.write("---\n")
    f.write('<div style="display:none">t1</div>\n\n')
    start = ''
    for k,v in sorted(papers, key=lambda x:(x[1]['year'],x[1]['sortauthor'],x[1]['title']),
            reverse=True):
        
        current = v['year']
        if current != start:
            start = current
            if start == 'forthcoming':
                f.write('<h2><a class="target_link" id="forthcoming">Papers to appear</a></h2>\n')
            else:
                f.write('<h2><a class="target_link" id="Papers{0}">Papers from {0}</a></h2>\n'.format(start))

        out = bib.format(k, template='html')
        f.write('<li id="{0}" class="paper">'.format(k))
        f.write(out+'\n')
        tmp = '  <p class="resources">'
        for key,value in sorted(v.items()):
            if key.startswith('_'):
                name = key[1:].upper()
                tmp += '<span><a class="resource '+name.lower()+'" target="_blank" '
                tmp += 'href="'+v[key]+'">'+name+'</a></span>'
        if v['type'] != 'misc':
            tmp += '<span id="'+k+'" onclick="showBibTex(event,'+"'"+k+"'"+')">'
            tmp += '<a class="resource bibtex" target="_blank" '
            tmp += 'href="http://bibliography.lingpy.org/raw.php?key='
            tmp += k+'&view=raw">BibTex</a></span>'
        tmp += '</p>'
        if tmp:
            f.write(tmp+'</li>\n')
        else:
            f.write('</li>\n')
f.close()
        

# write talks to file
with open('../talks.md', 'w') as f:
    f.write("---\n")
    f.write("title: Talks\n")
    f.write("type: research\n")
    f.write("layout: default\n")
    f.write("---\n")
    f.write('<div style="display:none">t2</div>\n\n')
    f.write('<script src="media/jquery.fancybox.js"></script>\n')
    f.write('<link rel="stylesheet" type="text/css" href="{{ site.baseurl }}/css/jquery.fancybox.css" />\n')
    start = ''
    for k,v in sorted(talks, key=lambda x:(x[1]['year'],x[1]['eventdate']),
            reverse=True):
        
        current = v['year']
        if current != start:
            start = current
            if start == 'forthcoming':
                f.write('## Talks to appear\n \n')
            else:
                f.write('## Talks from {0}\n \n'.format(start))

        out = bib.format(k, template='html')
        f.write('<li class="paper">'+out+'\n')
        tmp = '  <p class="resources">'
        for key,value in sorted(v.items()):
            if key.startswith('_'):
                name = key[1:].upper()
                if key == '_slides':
                    tmp += '<span><a class="resource slides fancybox fancybox.iframe" '
                else:
                    tmp += '<span><a class="resource '+name.lower()+'" target="_blank" '
                tmp += 'href="'+v[key]+'">'+name+'</a></span>'
        tmp += '</p>'
        if tmp:
            f.write(tmp+'</li>\n')
        else:
            f.write('</li>\n')
    f.write("""
<script>
$(".fancybox").fancybox({
    type: "iframe",
    fitToView: false
});
</script>
            """)


# write lectures to file
with open('../teaching.md', 'w') as f:
    f.write("---\n")
    f.write("title: Teaching\n")
    f.write("status: toplevelnc\n")
    f.write("layout: default\n")
    f.write("---\n")
    f.write('<div style="display:none">t4</div>\n\n')
    start = ''
    for k,v in sorted(lectures, key=lambda x:(x[1]['year'],x[1]['term'],x[1]['title']),
            reverse=True):
        
        current = v['term'] + ' Term '+v['year']
        if current != start:
            start = current
            if start == 'forthcoming':
                f.write('## Forthcoming lectures\n \n')
            else:
                f.write('## {0}\n \n'.format(start))

        out = bib.format(k, template='html')
        f.write('<li class="paper">'+out+'\n')
        tmp = '  <p class="resources">'
        for key,value in sorted(v.items()):
            if key.startswith('_'):
                name = key[1:].upper()
                tmp += '<span><a class="resource '+name.lower()+'" target="_blank" '
                tmp += 'href="'+v[key]+'">'+name+'</a></span>'
        if tmp:
            f.write(tmp+'</li>\n')
        else:
            f.write('</li>\n')
f.close()

# write lectures to latex file
with open('../cv/courses-german.tex', 'w') as f:
    start = ''
    started = False
    for k,v in sorted(lectures, key=lambda x:(x[1]['year'],x[1]['term'],x[1]['title']),
            reverse=True):
        
        current = v['term'].replace('Summer','Sommer') + 'semester '+v['year']
        if current != start:
            start = current
            if start == 'forthcoming':
                f.write(r'\noindent\textit{{Zukünftige Seminare}}\par'+'\n')
            else:
                f.write(r'\noindent\textit{{{0}}}\par\nopagebreak\vspace{{0.25cm}}'.format(start))
                f.write('\n')
        
        out = bib.format(k, template='tex')
        f.write(r'\nopagebreak\noindent '+out+r'\vspace{0.25cm}'+'\n')
        
        f.write(r'\par'+'\n')
f.close()

# write lectures to latex file
with open('../cv/papers-german.tex', 'w') as f:
    start = ''
    for k,v in sorted(papers, key=lambda x:(x[1]['year'],x[1]['sortauthor'],x[1]['title']),
            reverse=True):
        
        current = v['year']
        if current != start:
            start = current
            if start == 'forthcoming':
                f.write(r'\noindent\textit{{Im Erscheinen}}\par\nopagebreak\vspace{0.25cm}')
                f.write('\n')
            else:
                f.write(r'\noindent\textit{{{0}}}\par\nopagebreak\vspace{{0.25cm}}'.format(start))
                f.write('\n')
        #f.write(r'\begin{itemize}'+'\n')
        out = bib.format(k, template='tex')
        f.write(r'\nopagebreak\noindent '+out+r'\vspace{0.25cm}'+'\n')

        f.write(r'\par'+'\n')
f.close()
