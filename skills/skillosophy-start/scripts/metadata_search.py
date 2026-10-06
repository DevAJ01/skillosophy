"""Cheap metadata relevance; scores are not effectiveness evidence."""
import collections,math,re

STOP={'a','an','the','to','for','and','or','of','in','with','my','our','build','project','use','skill','skills','when','that','this','is','it','on','from','be','as','by','you','your','are','existing','current','new','adding','before','complete','validation','acceptance','form','bulk','edit','stack'}

def tokens(text):return [t for t in re.findall(r'[a-z0-9]+',text.lower()) if t not in STOP]

DOMAINS={
 'frontend':('frontend','react','nextjs','angular','vue','tailwind','css','ui','a11y','accessibility'),
 'database':('database','postgres','postgresql','sql','sqlite','mysql','schema','migration'),
 'api':('api','backend','graphql','grpc','http','rest'),
 'testing':('test','testing','playwright','pytest','cypress','jest','qa'),
 'ai':('rag','llm','ai','prompt','agent','mcp','machine-learning'),
 'devops':('deploy','devops','docker','kubernetes','terraform','azure','aws','cloud','ci','cd'),
 'security':('security','auth','oauth','vulnerability','pentest','threat'),
 'business':('marketing','sales','finance','product','business','revenue','seo','growth','strategy','research')}

def domain_match(entry,domain):
 name_terms=set(tokens(entry['name']))
 category=set(tokens(entry['category']))
 return any(k in name_terms or k in category or ('-' in k and k in entry['name']) for k in DOMAINS[domain])

def rank_metadata(es,query,limit=8,domain=None):
 if domain and domain not in DOMAINS:raise ValueError('Unsupported project capability domain')
 es=[e for e in es if not domain or domain_match(e,domain)]
 docs=[collections.Counter(tokens(e['name'].replace('-',' ')+' '+e.get('description','')+' '+e.get('category',''))) for e in es]
 df=collections.Counter(t for d in docs for t in d);avg=sum(sum(d.values()) for d in docs)/max(len(docs),1)
 qs=set(tokens(query));results=[]
 for e,d in zip(es,docs):
  n=sum(d.values());score=0;matched=[]
  for t in qs:
   tf=d[t]
   if not tf:continue
   matched.append(t);idf=math.log(1+(len(es)-df[t]+.5)/(df[t]+.5))
   score+=idf*tf*2.2/(tf+1.2*(.25+.75*n/max(avg,1)))
   if t in tokens(e['name']):score+=idf*.5
  if score:results.append({**e,'score':round(score,5),'matched_terms':sorted(matched)})
 results.sort(key=lambda e:(-e['score'],e['name']))
 return results[:limit]
